"""Application module."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from admin import endpoints 

from admin.machine_assets.machine_setup.defect_rate.endpoints import defect_rate_endpoint
from admin.machine_assets.machine_setup.line_quality.endpoints import line_quality_endpoint

from containers import Container


def create_app() -> FastAPI:
    container = Container()
    db = container.db()
    db.create_database()

    # Register provider
    container.providers["kpi_defect_rate_service"] = container.kpi_defect_rate_service
    container.providers["KPILineProductionQualityService"] = container.KPILineProductionQualityService
    
    # Wire container
    container.wire(
        modules=[
            "admin.machine_assets.machine_setup.defect_rate.endpoints.defect_rate_endpoint",
            "admin.machine_assets.machine_setup.line_quality.endpoints.line_quality_endpoint"
        ]
    )

    app = FastAPI()

    app.include_router(endpoints.router, prefix="/auth", tags=["auth"])
    app.include_router(defect_rate_endpoint.router)  
    app.include_router(line_quality_endpoint.router)  
    return app


app = create_app()