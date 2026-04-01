"""Containers module."""

from dependency_injector import containers, providers
from fastapi.security import OAuth2PasswordBearer
import os
from admin.machine_assets.machine_setup.defect_rate.repositories import defect_rate_repository
from admin.machine_assets.machine_setup.defect_rate.services import defect_rate_services

from admin.machine_assets.machine_setup.line_quality.repositories import line_quality_repository
from admin.machine_assets.machine_setup.line_quality.services import line_quality_services

from database import Database
from auth_client.auth_service import AuthService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "admin.machine_assets.machine_setup.defect_rate.endpoints.defect_rate_endpoint",
            "admin.machine_assets.machine_setup.line_quality.services.line_quality_services",
            "auth_client.endpoints",
            "auth_client.dependencies"
        ],
        packages=[],
    )

    oauth2_scheme = providers.Object(OAuth2PasswordBearer(tokenUrl="auth/token"))
    config = providers.Configuration(yaml_files=["config.yml"])
    # db = providers.Singleton(Database, db_url=config.db.url)
    db_url = os.environ.get("DATABASE_URL") or config.db.url
    db = providers.Singleton(Database, db_url)
    
    auth_service = providers.Factory(
        AuthService,
        db=db,
    )

    
    kpi_defect_rate_repository = providers.Factory(
        defect_rate_repository.KPIDefectRateRepository,
        session_factory = db.provided.session,
        bookings_url=config.bookings_url.from_value("https://core_demo.momes-solutions.com/bookings/bookings/")
    )
    
 
    kpi_defect_rate_service = providers.Factory(
        defect_rate_services.KPIDefectRateService,
        kpi_defect_rate_repository=kpi_defect_rate_repository
    )
    
    KPILineProductionQualityRepository = providers.Factory(
        line_quality_repository.KPILineProductionQualityRepository,
        session_factory = db.provided.session,
        bookings_url=config.bookings_url.from_value("https://core_demo.momes-solutions.com/bookings/bookings/"),
        lines_url=config.lines_url.from_value("https://core_demo.momes-solutions.com/lines/lines/")
    )
    
 
    KPILineProductionQualityService = providers.Factory(
        line_quality_services.KPILineProductionQualityService,
        KPILineProductionQualityRepository=KPILineProductionQualityRepository
    )


    def init_resources(self):
        """Initialize resources like database tables."""
        db = self.db()
        db.create_database()