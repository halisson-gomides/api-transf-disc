from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, Depends, WebSocket
from fastapi.websockets import WebSocketDisconnect
import orjson
from fastapi.responses import RedirectResponse, ORJSONResponse, HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
import logging
from cashews.contrib.fastapi import (
    CacheEtagMiddleware,
    CacheRequestControlMiddleware    
)
from collections import defaultdict
from src.database import Database
from src.cache import setup_cache
from src.utils import reset_minute_counters, verify_admin, config, save_stats
import asyncio
import psutil
import json
import time
import datetime as dt


# Importando Rotas
from src.routers.programa import pg_router
from src.routers.proponente import prop_router
from src.routers.proposta import prtas_router
from src.routers.justificativas_proposta import jus_prop_router
from src.routers.proposta_cancelada import prop_cancel_router
from src.routers.proposta_selecao_pac import psp_router
from src.routers.pergunta_selecao_pac import persp_router
from src.routers.resposta_selecao_pac import ressp_router
from src.routers.proposta_formalizacao_pac import prpfpac_router
from src.routers.plano_aplicacao_detalhado import plapdet_router
from src.routers.meta_crono_fisico import meta_crono_fisico_router
from src.routers.etapa_crono_fisico import etapa_crono_fisico_router
from src.routers.convenio import convenio_router
from src.routers.historico_situacao import historico_situacao_router
from src.routers.termo_aditivo import termo_aditivo_router
from src.routers.prorroga_oficio import prorroga_oficio_router
from src.routers.empenho import empenho_router
from src.routers.desembolso import desembolso_router
from src.routers.cronograma_desembolso import crono_router
from src.routers.ingresso_contrapartida import ingresso_contrapartida_router
from src.routers.desbloqueio_cr import desbloqueio_cr_router
from src.routers.pagamento import pagamento_router
from src.routers.obtv_convenente import obtv_convenente_router
from src.routers.pagamento_tributo import pagamento_tributo_router
from src.routers.emenda import emenda_router
from src.routers.licitacao import licitacao_router
from src.routers.contrato import contrato_router
from src.routers.historico_projeto_basico import historico_projeto_basico_router
from src.routers.resumo_fisico_financeiro import resumo_fisico_financeiro_router
from src.routers.solicitacao_ajuste_pt import solicitacao_ajuste_pt_router
from src.routers.solicitacao_alteracao import solicitacao_alteracao_router
from src.routers.solicitacao_rendimento_aplicacao import solicitacao_rendimento_aplicacao_router
from src.routers.coordenadas_obra import coordenadas_obra_router
from src.routers.acomp_obras_contratos_medicoes_modulo_empresas import acomp_obras_contratos_medicoes_modulo_empresas_router
from src.routers.acomp_obras_valores_itens_medicao_modulo_empresas import acomp_obras_valores_itens_medicao_modulo_empresas_router
from src.routers.inst_cont_proposta_aio_modulo_empresas import inst_cont_proposta_aio_modulo_empresas_router
from src.routers.inst_cont_contratos_lotes_empresas_modulo_empresas import inst_cont_contratos_lotes_empresas_modulo_empresas_router
from src.routers.inst_cont_metas_submetas_po_modulo_empresas import inst_cont_metas_submetas_po_modulo_empresas_router
from src.routers.projeto_basico_acffo_modulo_empresas import projeto_basico_acffo_modulo_empresas_router
from src.routers.projeto_basico_lae_modulo_empresas import projeto_basico_lae_modulo_empresas_router
from src.routers.projeto_basico_metas_modulo_empresas import projeto_basico_metas_modulo_empresas_router
from src.routers.projeto_basico_proposta_modulo_empresas import projeto_basico_proposta_modulo_empresas_router
from src.routers.projeto_basico_submetas_modulo_empresas import projeto_basico_submetas_modulo_empresas_router



# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize instances
db = Database()
# Initialize a dictionary to store request counts and timings
request_stats = defaultdict(lambda: {"count": 0, "total_time": 0, "last_minute_count": 0, "up_time": 0})
monthly_stats = defaultdict(int)
excluded_stats_paths = ["/", "/stats", "/docs", "/static/icon.jpg", "/openapi.json", "/favicon.ico"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load before the app starts
    logger.info("Iniciando aplicação...")
    try:
        # Inicializa o Banco de Dados
        await db.init_db()        
        # Configure o cache
        setup_cache(config)
        # background task to reset the "last minute" counters every 60 seconds.
        reset_task = asyncio.create_task(reset_minute_counters(request_stats))
        save_task = asyncio.create_task(save_stats(monthly_stats))
        # setting app uptime with timezone offset
        _app_uptime = time.time() - 3*3600
        request_stats["/"]["up_time"] = time.strftime("%d/%m/%Y %H:%M", time.localtime(_app_uptime))
        logger.info("Aplicação iniciada com sucesso!")
    except Exception as e:
        logger.error(f"Erro na inicialização: {str(e)}")
        raise
    yield
    # load after the app has finished
    # Shutdown: Cancel the background task
    reset_task.cancel()
    save_task.cancel()
    try:
        await reset_task
        await save_task
    except asyncio.CancelledError:
        pass
    

app = FastAPI(lifespan=lifespan, 
              docs_url=None, 
              title=config.APP_NAME, 
              description=config.APP_DESCRIPTION,
              openapi_tags=config.APP_TAGS,
              default_response_class=ORJSONResponse)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluindo Middlewares
app.add_middleware(CacheEtagMiddleware)
app.add_middleware(CacheRequestControlMiddleware)


@app.middleware("http")
async def track_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Update stats
    path = request.url.path
    if path in excluded_stats_paths:
        return response
    
    _curr_date = dt.datetime.now(tz=dt.timezone(dt.timedelta(hours=-3)))
    _curr_month = _curr_date.strftime("%m/%Y")
    monthly_stats[_curr_month] += 1
    request_stats[path]["count"] += 1
    request_stats[path]["total_time"] += process_time
    request_stats[path]["last_minute_count"] += 1
    
    return response


# Incluindo Rotas
app.include_router(pg_router)
app.include_router(prop_router)
app.include_router(prtas_router)
app.include_router(jus_prop_router)
app.include_router(prop_cancel_router)
app.include_router(psp_router)  
app.include_router(persp_router)
app.include_router(ressp_router)
app.include_router(prpfpac_router)
app.include_router(plapdet_router)
app.include_router(meta_crono_fisico_router)
app.include_router(etapa_crono_fisico_router)
app.include_router(convenio_router)
app.include_router(historico_situacao_router)
app.include_router(termo_aditivo_router)
app.include_router(prorroga_oficio_router)
app.include_router(empenho_router)
app.include_router(desembolso_router)
app.include_router(crono_router)
app.include_router(ingresso_contrapartida_router)
app.include_router(desbloqueio_cr_router)
app.include_router(pagamento_router)
app.include_router(obtv_convenente_router)
app.include_router(pagamento_tributo_router)
app.include_router(emenda_router)
app.include_router(licitacao_router)
app.include_router(contrato_router)
app.include_router(historico_projeto_basico_router)
app.include_router(resumo_fisico_financeiro_router)
app.include_router(solicitacao_ajuste_pt_router)
app.include_router(solicitacao_alteracao_router)
app.include_router(solicitacao_rendimento_aplicacao_router)
app.include_router(coordenadas_obra_router)
app.include_router(acomp_obras_contratos_medicoes_modulo_empresas_router)
app.include_router(acomp_obras_valores_itens_medicao_modulo_empresas_router)
app.include_router(inst_cont_proposta_aio_modulo_empresas_router)
app.include_router(inst_cont_contratos_lotes_empresas_modulo_empresas_router)
app.include_router(inst_cont_metas_submetas_po_modulo_empresas_router)
app.include_router(projeto_basico_acffo_modulo_empresas_router)
app.include_router(projeto_basico_lae_modulo_empresas_router)
app.include_router(projeto_basico_metas_modulo_empresas_router)
app.include_router(projeto_basico_proposta_modulo_empresas_router)
app.include_router(projeto_basico_submetas_modulo_empresas_router)



@app.get("/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=config.APP_NAME + " - Documentação",        
        swagger_favicon_url="/static/icon.jpg",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1}
    )


@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.get("/stats", include_in_schema=False, response_class=HTMLResponse)
async def get_stats(username: str = Depends(verify_admin)):
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage('/').percent
    app_uptime = request_stats["/"]["up_time"]
    html_content = f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>API Stats</title>
                <link rel="icon" type="image/x-icon" href="/static/icon.jpg">
                <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>   
                <style>
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                    }}
                    th, td {{
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    .chart-container {{
                        width: 100%;
                        max-width: 800px;
                        margin: 20px auto;
                        padding: 15px;
                        background-color: #f8f9fa;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}
                    .chart-title {{
                        text-align: center;
                        color: #333;
                        margin-bottom: 15px;
                        font-family: Arial, sans-serif;
                    }}
                    #monthlyRequestsChart {{
                        border-radius: 5px;
                        background-color: white;
                    }}
                </style>             
            </head>
            <body>
                <header>
                    <h1>API-Discricionárias e Legais - Estatísticas</h1>
                    <p>Estatísticas relativas aos endpoints do serviço de API</p>
                </header>
                <main>
                <div class="chart-container">
                    <h5 class="chart-title">Requisições por Minuto</h5>
                    <canvas id="requestsChart" width="100px" height="40px"></canvas>
                </div>
                <div class="chart-container">
                    <h5 class="chart-title">Requisições Mensais</h5>
                    <canvas id="monthlyRequestsChart" width="100px" height="40px"></canvas>
                </div>
                <h2>Endpoint Stats</h2>
                <h3>Since: {app_uptime}</h3>
                <table id="endpointStats">
                    <thead>
                        <tr>
                            <th>Endpoint</th>
                            <th>Total Requests</th>
                            <th>Requests/Minute</th>
                            <th>Avg Response Time (ms)</th>
                        </tr>
                    </thead>
                    <tbody>
        """

    for path, stats in request_stats.items():   
        if path in excluded_stats_paths:
            continue     
        avg_time = stats["total_time"] / stats["count"] if stats["count"] > 0 else 0
        html_content += f"""
                <tr data-path="{path}">
                    <td>{path}</td>
                    <td>{stats['count']}</td>
                    <td>{stats['last_minute_count']}</td>
                    <td>{avg_time * 1000:.2f}</td>
                </tr>
        """

    html_content += """
                </tbody>
            </table>
            <h2>System Resources</h2>
            <table id="systemStats">
                <thead>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>CPU Usage</td>
                        <td id="cpu-usage">{cpu_percent}%</td>
                    </tr>
                    <tr>
                        <td>Memory Usage</td>
                        <td id="memory-usage">{memory_percent}%</td>
                    </tr>
                    <tr>
                        <td>Disk Usage</td>
                        <td id="disk-usage">{disk_percent}%</td>
                    </tr>
                </tbody>
            </table>
            </main>
            <footer>
                <p>Coordenacao-geral de Informacao e Monitoramento de Obras - CGIMO<br>
                Diretoria de Transferências e Parcerias da União - DTPAR/SEGES/MGI</p>                
            </footer>
            <script>
                // Get chart context and create the chart
                const ctx = document.getElementById('requestsChart').getContext('2d');
                const perMinuteChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: [], // Endpoint names
                        datasets: [{
                            label: 'Requests per Minute',
                            data: [],  // Requests per minute for each endpoint
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        indexAxis: 'y', // Esta opção inverte os eixos, criando um gráfico horizontal
                        responsive: true,                        
                        plugins: {                            
                            legend: {
                                display: false // Oculta a legenda se não for necessária
                            }
                        },
                        scales: {
                            x: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Requests/Minute'
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Endpoint'
                                }
                            }
                        }
                    }
                });

                const ctxMonthly = document.getElementById('monthlyRequestsChart').getContext('2d');
                const perMonthChart = new Chart(ctxMonthly, {
                    type: 'bar',
                    data: {
                        labels: [], // Month names
                        datasets: [{
                            label: 'Requests per Month',
                            data: [],  // Total amount Requests per month
                            backgroundColor: 'rgba(44, 108, 192, 0.5)',
                            borderColor: 'rgba(44, 108, 192, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,                        
                        plugins: {                            
                            legend: {
                                display: false // Oculta a legenda se não for necessária
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Requests/Month'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Month'
                                }
                            }
                        }
                    }
                });

                // Initialize WebSocket connection
                const socket = new WebSocket("ws://localhost:8000/ws");

                // Handle WebSocket messages
                socket.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    updateStats(data);
                };

                // Function to update the per minute chart with new data
                function updateMinuteChart(data) {
                    // Extract endpoint names and requests per minute
                    const endpointNames = Object.keys(data.endpoints);
                    const requestsPerMinute = Object.values(data.endpoints).map(stats => stats.last_minute_count);

                    // Update chart data
                    perMinuteChart.data.labels = endpointNames;
                    perMinuteChart.data.datasets[0].data = requestsPerMinute;

                    // Refresh the chart
                    perMinuteChart.update();
                }

                // Function to update the monthly chart with new data
                function updateMonthlyChart(data) {
                    const parseDate = (dateStr) => {
                        const [month, year] = dateStr.split('/');
                        return new Date(year, parseInt(month) - 1, 1);
                    };

                    const now = new Date();
                    const twoYearsAgo = new Date(now.getFullYear() - 2, now.getMonth(), 1);

                    const months = Object.keys(data.monthly)
                        .filter(monthStr => parseDate(monthStr) >= twoYearsAgo)
                        .sort((a, b) => parseDate(a) - parseDate(b));

                    const requestCounts = months.map(month => data.monthly[month]);

                    perMonthChart.data.labels = months; // Mantém os labels originais (MM/YYYY)
                    perMonthChart.data.datasets[0].data = requestCounts;
                    perMonthChart.update();
                }

                // Function to update the stats page with new data
                function updateStats(data) {
                    // Update endpoint stats table
                    const table = document.getElementById('endpointStats');
                    const tbody = table.querySelector('tbody'); // Target tbody for dynamic updates

                    for (const [path, stats] of Object.entries(data.endpoints)) {
                         
                        let row = tbody.querySelector(`tr[data-path="${path}"]`); // Search within tbody
                        if (!row) {
                            // Create a new row if it doesn't exist
                            row = tbody.insertRow(); // Insert into tbody
                            row.setAttribute('data-path', path);
                            for (let i = 0; i < 4; i++) {
                                row.insertCell();
                            }
                            row.cells[0].textContent = path; // Set endpoint name
                        }
                        row.cells[1].textContent = stats.count; // Update Total Requests
                        row.cells[2].textContent = stats.last_minute_count; // Update Requests/Minute
                        row.cells[3].textContent = stats.avg_time.toFixed(2); // Update Avg Response Time
                    }

                    // Update system stats
                    document.getElementById("cpu-usage").textContent = data.system.cpu + "%";
                    document.getElementById("memory-usage").textContent = data.system.memory + "%";
                    document.getElementById("disk-usage").textContent = data.system.disk + "%";

                    // Update the chart
                    updateMinuteChart(data);
                    updateMonthlyChart(data);
                }
            </script>
        </body>
    </html>
    """  
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


@app.websocket("/ws")
async def stats_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send updated stats every second
            await asyncio.sleep(1)
            stats_data = {
                "endpoints": {
                    path: {
                        "count": stats["count"],
                        "last_minute_count": stats["last_minute_count"],
                        "avg_time": (stats["total_time"] / stats["count"] if stats["count"] > 0 else 0) * 1000
                    } for path, stats in request_stats.items() if path not in excluded_stats_paths
                },
                "system": {
                    "cpu": psutil.cpu_percent(),
                    "memory": psutil.virtual_memory().percent,
                    "disk": psutil.disk_usage('/').percent
                },
                "monthly": {
                    month: count for month, count in monthly_stats.items()
                }
            }
            await websocket.send_text(json.dumps(stats_data))
            
    except WebSocketDisconnect:
        pass


# Run in terminal
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-config log_conf.yaml --workers 4