from app.models.training.training import Training
from app.models.training.benefit import TrainingBenefit
from app.models.training.mentor import Mentor
from app.models.training.training_mentor import TrainingMentor

from app.models.services.service import Service
from app.models.services.service_offer import ServiceOffering
from app.models.services.service_teck import ServiceTech
from app.models.services.service_offer_map import ServiceOfferingMap
from app.models.services.service_tech_map import ServiceTechMap

from app.models.member.member import Member

from app.models.opportunities.opportunity import Opportunity
from app.models.opportunities.requirement import OpportunityRequirement
from app.models.opportunities.job import JobDetail
from app.models.opportunities.internship import InternshipDetail

from app.models.projects.project import Project
from app.models.projects.feedback import ProjectFeedback
from app.models.projects.project_tech_map import ProjectTechMap

# auth models (already working)
from .login_model import AdminUser