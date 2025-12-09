#!/usr/bin/env python3

"""
On-Call Tenant Architecture Report Generator
Creates a comprehensive PDF report explaining the on-call tenant architecture
in the case_management domain including services, deployment, and databases
for both staging and production environments.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np
from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, blue, red, green, orange, purple
import io
import os

class OnCallTenantReportGenerator:
    def __init__(self):
        self.pdf_path = "/Users/agustin.fusaro/OnCall_Tenant_Architecture_Report.pdf"
        self.doc = SimpleDocTemplate(self.pdf_path, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=18)
        self.styles = getSampleStyleSheet()
        self.content = []
        
        # Define custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2E86C1')
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=HexColor('#1B4F72')
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            textColor=HexColor('#2E86C1')
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leading=12
        )
        
        self.code_style = ParagraphStyle(
            'CodeStyle',
            parent=self.styles['Code'],
            fontSize=9,
            fontName='Courier',
            leftIndent=20,
            backColor=HexColor('#F8F9FA'),
            borderColor=HexColor('#E9ECEF'),
            borderWidth=1,
            borderPadding=6
        )

    def create_tenant_overview_diagram(self):
        """Create a diagram showing the overall tenant architecture"""
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'Case Management Multi-Tenant Architecture', 
                fontsize=16, fontweight='bold', ha='center')
        
        # Case Management Tenant (Left Side)
        cm_box = FancyBboxPatch((0.5, 6), 3.5, 2.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#E8F4FD', edgecolor='#2E86C1', linewidth=2)
        ax.add_patch(cm_box)
        ax.text(2.25, 7.8, 'Case Management Tenant', fontsize=12, fontweight='bold', ha='center')
        ax.text(2.25, 7.4, 'Work Type: CASE', fontsize=10, ha='center')
        ax.text(2.25, 7.0, 'Statuses: OPEN, IN_PROGRESS, CLOSED', fontsize=9, ha='center')
        ax.text(2.25, 6.6, 'DB: case-management', fontsize=9, ha='center')
        ax.text(2.25, 6.2, 'ES: elasticsearch-casem-v8', fontsize=9, ha='center')
        
        # On-Call Tenant (Right Side)
        oc_box = FancyBboxPatch((6, 6), 3.5, 2.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#FFF3E0', edgecolor='#FF8F00', linewidth=2)
        ax.add_patch(oc_box)
        ax.text(7.75, 7.8, 'On-Call Tenant', fontsize=12, fontweight='bold', ha='center')
        ax.text(7.75, 7.4, 'Work Type: PAGE', fontsize=10, ha='center')
        ax.text(7.75, 7.0, 'Statuses: TRIGGERED, ACKNOWLEDGED, RESOLVED', fontsize=9, ha='center')
        ax.text(7.75, 6.6, 'DB: case-management-oncall', fontsize=9, ha='center')
        ax.text(7.75, 6.2, 'ES: elasticsearch-casem-oncall', fontsize=9, ha='center')
        
        # Shared Components
        shared_box = FancyBboxPatch((2, 4), 6, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#F3E5F5', edgecolor='#8E24AA', linewidth=2)
        ax.add_patch(shared_box)
        ax.text(5, 5, 'Shared Components', fontsize=12, fontweight='bold', ha='center')
        ax.text(3, 4.6, '• Common Codebase', fontsize=10, ha='left')
        ax.text(3, 4.3, '• Tenant-Aware Business Logic', fontsize=10, ha='left')
        ax.text(6, 4.6, '• Query Handlers', fontsize=10, ha='left')
        ax.text(6, 4.3, '• ES Mappings', fontsize=10, ha='left')
        
        # Service Instances
        ax.text(5, 3.5, 'Service Deployment Strategy', fontsize=12, fontweight='bold', ha='center')
        
        # Case Management Services
        cm_service_box = FancyBboxPatch((1, 1.5), 3, 1.5, 
                                       boxstyle="round,pad=0.1", 
                                       facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=1)
        ax.add_patch(cm_service_box)
        ax.text(2.5, 2.6, 'Case Management Services', fontsize=10, fontweight='bold', ha='center')
        ax.text(1.2, 2.3, '• case-api.case-management.*', fontsize=8, ha='left')
        ax.text(1.2, 2.0, '• case-event-relay.case-management.*', fontsize=8, ha='left')
        ax.text(1.2, 1.7, '• Domain Events: domain-events', fontsize=8, ha='left')
        
        # On-Call Services
        oc_service_box = FancyBboxPatch((6, 1.5), 3, 1.5, 
                                       boxstyle="round,pad=0.1", 
                                       facecolor='#FFF8E1', edgecolor='#F57F17', linewidth=1)
        ax.add_patch(oc_service_box)
        ax.text(7.5, 2.6, 'On-Call Services', fontsize=10, fontweight='bold', ha='center')
        ax.text(6.2, 2.3, '• case-api-on-call.case-management.*', fontsize=8, ha='left')
        ax.text(6.2, 2.0, '• case-event-relay-on-call.case-management.*', fontsize=8, ha='left')
        ax.text(6.2, 1.7, '• Domain Events: domain-events-oncall', fontsize=8, ha='left')
        
        # Arrows showing tenant detection
        arrow1 = FancyArrowPatch((2.25, 5.8), (2.5, 3.1),
                                arrowstyle='->', mutation_scale=20, color='#2E86C1')
        ax.add_patch(arrow1)
        
        arrow2 = FancyArrowPatch((7.75, 5.8), (7.5, 3.1),
                                arrowstyle='->', mutation_scale=20, color='#FF8F00')
        ax.add_patch(arrow2)
        
        # Environment variable note
        env_box = FancyBboxPatch((1, 0.2), 8, 0.8, 
                                boxstyle="round,pad=0.05", 
                                facecolor='#FFFDE7', edgecolor='#FBC02D', linewidth=1)
        ax.add_patch(env_box)
        ax.text(5, 0.6, 'Tenant Detection: TENANT_NAME environment variable', 
                fontsize=10, fontweight='bold', ha='center')
        ax.text(5, 0.3, 'Default: "case-management" | On-Call: "on-call"', 
                fontsize=9, ha='center')
        
        plt.tight_layout()
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return img_buffer

    def create_database_architecture_diagram(self):
        """Create a diagram showing database architecture for both environments"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
        
        # Staging Environment
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        ax1.axis('off')
        ax1.text(5, 9.5, 'Staging Environment', fontsize=14, fontweight='bold', ha='center')
        
        # Case Management DB (Staging)
        cm_db_box = FancyBboxPatch((1, 7), 3.5, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
        ax1.add_patch(cm_db_box)
        ax1.text(2.75, 8, 'Case Management DB', fontsize=10, fontweight='bold', ha='center')
        ax1.text(2.75, 7.6, 'Host: case-management-db.postgres', fontsize=8, ha='center')
        ax1.text(2.75, 7.3, '.us1.staging.dog:5433', fontsize=8, ha='center')
        
        # On-Call DB (Staging)
        oc_db_box = FancyBboxPatch((5.5, 7), 3.5, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor='#FFF8E1', edgecolor='#F57F17', linewidth=2)
        ax1.add_patch(oc_db_box)
        ax1.text(7.25, 8, 'On-Call DB', fontsize=10, fontweight='bold', ha='center')
        ax1.text(7.25, 7.6, 'Host: case-management-oncall-db', fontsize=8, ha='center')
        ax1.text(7.25, 7.3, '.postgres.us1.staging.dog:5433', fontsize=8, ha='center')
        
        # Database Details (Staging)
        details_box1 = FancyBboxPatch((1, 5), 8, 1.5, 
                                     boxstyle="round,pad=0.1", 
                                     facecolor='#F5F5F5', edgecolor='#757575', linewidth=1)
        ax1.add_patch(details_box1)
        ax1.text(5, 6.2, 'Database Configuration Details', fontsize=11, fontweight='bold', ha='center')
        ax1.text(1.5, 5.8, 'Case Management:', fontsize=9, fontweight='bold', ha='left')
        ax1.text(1.5, 5.5, '• User: case_management', fontsize=8, ha='left')
        ax1.text(1.5, 5.2, '• Cluster: case-management', fontsize=8, ha='left')
        ax1.text(5.5, 5.8, 'On-Call:', fontsize=9, fontweight='bold', ha='left')
        ax1.text(5.5, 5.5, '• User: case_management_oncall', fontsize=8, ha='left')
        ax1.text(5.5, 5.2, '• Cluster: case-management-oncall', fontsize=8, ha='left')
        
        # Elasticsearch (Staging)
        es_box1 = FancyBboxPatch((1, 3), 8, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#E8F5E8', edgecolor='#4CAF50', linewidth=2)
        ax1.add_patch(es_box1)
        ax1.text(5, 4.2, 'Elasticsearch Clusters', fontsize=11, fontweight='bold', ha='center')
        ax1.text(1.5, 3.8, 'Case Management ES:', fontsize=9, fontweight='bold', ha='left')
        ax1.text(1.5, 3.5, '• Cluster: elasticsearch-casem-v8', fontsize=8, ha='left')
        ax1.text(1.5, 3.2, '• Index: cases', fontsize=8, ha='left')
        ax1.text(5.5, 3.8, 'On-Call ES:', fontsize=9, fontweight='bold', ha='left')
        ax1.text(5.5, 3.5, '• Cluster: elasticsearch-casem-oncall', fontsize=8, ha='left')
        ax1.text(5.5, 3.2, '• Index: cases (separate)', fontsize=8, ha='left')
        
        # Kafka Topics (Staging)
        kafka_box1 = FancyBboxPatch((1, 1), 8, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#FFF3E0', edgecolor='#FF8F00', linewidth=2)
        ax1.add_patch(kafka_box1)
        ax1.text(5, 2.2, 'Event Streaming (Kafka)', fontsize=11, fontweight='bold', ha='center')
        ax1.text(1.5, 1.8, 'Case Management:', fontsize=9, fontweight='bold', ha='left')
        ax1.text(1.5, 1.5, '• Topic: domain-events', fontsize=8, ha='left')
        ax1.text(1.5, 1.2, '• Event Relay: case-event-relay.*', fontsize=8, ha='left')
        ax1.text(5.5, 1.8, 'On-Call:', fontsize=9, fontweight='bold', ha='left')
        ax1.text(5.5, 1.5, '• Topic: domain-events-oncall', fontsize=8, ha='left')
        ax1.text(5.5, 1.2, '• Event Relay: case-event-relay-on-call.*', fontsize=8, ha='left')
        
        # Production Environment
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        ax2.axis('off')
        ax2.text(5, 9.5, 'Production Environment', fontsize=14, fontweight='bold', ha='center')
        
        # Case Management DB (Production)
        cm_db_box_prod = FancyBboxPatch((1, 7), 3.5, 1.5, 
                                       boxstyle="round,pad=0.1", 
                                       facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
        ax2.add_patch(cm_db_box_prod)
        ax2.text(2.75, 8, 'Case Management DB', fontsize=10, fontweight='bold', ha='center')
        ax2.text(2.75, 7.6, 'Host: case-management-db.postgres', fontsize=8, ha='center')
        ax2.text(2.75, 7.3, '.us1.prod.dog:5433', fontsize=8, ha='center')
        
        # On-Call DB (Production)
        oc_db_box_prod = FancyBboxPatch((5.5, 7), 3.5, 1.5, 
                                       boxstyle="round,pad=0.1", 
                                       facecolor='#FFF8E1', edgecolor='#F57F17', linewidth=2)
        ax2.add_patch(oc_db_box_prod)
        ax2.text(7.25, 8, 'On-Call DB', fontsize=10, fontweight='bold', ha='center')
        ax2.text(7.25, 7.6, 'Host: case-management-oncall-db', fontsize=8, ha='center')
        ax2.text(7.25, 7.3, '.postgres.us1.prod.dog:5433', fontsize=8, ha='center')
        
        # Multi-DC Deployment (Production)
        dc_box = FancyBboxPatch((1, 5), 8, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#FCE4EC', edgecolor='#E91E63', linewidth=2)
        ax2.add_patch(dc_box)
        ax2.text(5, 6.2, 'Multi-Datacenter Deployment', fontsize=11, fontweight='bold', ha='center')
        ax2.text(1.5, 5.8, 'Datacenters: us1, us3, us5, eu1, ap1, ap2', fontsize=9, ha='left')
        ax2.text(1.5, 5.5, 'Each DC has separate instances of both tenants', fontsize=9, ha='left')
        ax2.text(1.5, 5.2, 'Configuration per DC: config/k8s/values/tenants/', fontsize=9, ha='left')
        
        # High Availability (Production)
        ha_box = FancyBboxPatch((1, 3), 8, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#E8F5E8', edgecolor='#4CAF50', linewidth=2)
        ax2.add_patch(ha_box)
        ax2.text(5, 4.2, 'High Availability Features', fontsize=11, fontweight='bold', ha='center')
        ax2.text(1.5, 3.8, '• Master/Replica DB setup for both tenants', fontsize=9, ha='left')
        ax2.text(1.5, 3.5, '• Independent scaling per tenant', fontsize=9, ha='left')
        ax2.text(1.5, 3.2, '• Separate failure domains', fontsize=9, ha='left')
        
        # Monitoring & Observability (Production)
        monitor_box = FancyBboxPatch((1, 1), 8, 1.5, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor='#F3E5F5', edgecolor='#9C27B0', linewidth=2)
        ax2.add_patch(monitor_box)
        ax2.text(5, 2.2, 'Monitoring & Observability', fontsize=11, fontweight='bold', ha='center')
        ax2.text(1.5, 1.8, '• Per-tenant metrics and dashboards', fontsize=9, ha='left')
        ax2.text(1.5, 1.5, '• Separate alerting rules', fontsize=9, ha='left')
        ax2.text(1.5, 1.2, '• Independent SLA tracking', fontsize=9, ha='left')
        
        plt.tight_layout()
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return img_buffer

    def create_service_architecture_diagram(self):
        """Create a diagram showing service architecture and data flow"""
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        # Title
        ax.text(6, 11.5, 'On-Call Tenant Service Architecture & Data Flow', 
                fontsize=16, fontweight='bold', ha='center')
        
        # External Systems
        external_box = FancyBboxPatch((0.5, 9.5), 11, 1.5, 
                                     boxstyle="round,pad=0.1", 
                                     facecolor='#FFF3E0', edgecolor='#FF8F00', linewidth=2)
        ax.add_patch(external_box)
        ax.text(6, 10.6, 'External Integrations', fontsize=12, fontweight='bold', ha='center')
        ax.text(1, 10.2, '• Datadog On-Call API (/api/unstable/on-call/pages)', fontsize=10, ha='left')
        ax.text(1, 9.8, '• Escalation Policies & Teams', fontsize=10, ha='left')
        ax.text(7, 10.2, '• Phone/SMS/Email Notifications', fontsize=10, ha='left')
        ax.text(7, 9.8, '• Slack/PagerDuty Integrations', fontsize=10, ha='left')
        
        # API Gateway Layer
        api_box = FancyBboxPatch((2, 8), 8, 1, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
        ax.add_patch(api_box)
        ax.text(6, 8.5, 'API Layer: case-api-on-call.case-management.*.fabric.dog:6481', 
                fontsize=11, fontweight='bold', ha='center')
        
        # Application Services Layer
        app_services_box = FancyBboxPatch((1, 6), 10, 1.5, 
                                         boxstyle="round,pad=0.1", 
                                         facecolor='#F3E5F5', edgecolor='#9C27B0', linewidth=2)
        ax.add_patch(app_services_box)
        ax.text(6, 7.2, 'Application Services', fontsize=12, fontweight='bold', ha='center')
        ax.text(1.5, 6.8, '• Query Processors (Search, Analytics, Facets)', fontsize=10, ha='left')
        ax.text(1.5, 6.5, '• Case Management (CREATE, UPDATE, DELETE)', fontsize=10, ha='left')
        ax.text(1.5, 6.2, '• On-Call Specific Logic (Escalation, Acknowledgment)', fontsize=10, ha='left')
        ax.text(6.5, 6.8, '• Project Settings (Auto-assignment)', fontsize=10, ha='left')
        ax.text(6.5, 6.5, '• User Resolution & Team Management', fontsize=10, ha='left')
        ax.text(6.5, 6.2, '• Event Processing & Deduplication', fontsize=10, ha='left')
        
        # Data Storage Layer
        # PostgreSQL
        pg_box = FancyBboxPatch((0.5, 4), 3.5, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#E8F5E8', edgecolor='#4CAF50', linewidth=2)
        ax.add_patch(pg_box)
        ax.text(2.25, 5, 'PostgreSQL', fontsize=11, fontweight='bold', ha='center')
        ax.text(2.25, 4.6, 'case-management-oncall-db', fontsize=10, ha='center')
        ax.text(2.25, 4.3, '• Cases & Pages', fontsize=9, ha='center')
        ax.text(2.25, 4.1, '• On-Call Properties', fontsize=9, ha='center')
        
        # Elasticsearch
        es_box = FancyBboxPatch((4.25, 4), 3.5, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor='#FFFDE7', edgecolor='#FBC02D', linewidth=2)
        ax.add_patch(es_box)
        ax.text(6, 5, 'Elasticsearch', fontsize=11, fontweight='bold', ha='center')
        ax.text(6, 4.6, 'elasticsearch-casem-oncall', fontsize=10, ha='center')
        ax.text(6, 4.3, '• Search & Analytics', fontsize=9, ha='center')
        ax.text(6, 4.1, '• Faceted Search', fontsize=9, ha='center')
        
        # Kafka
        kafka_box = FancyBboxPatch((8, 4), 3.5, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor='#FCE4EC', edgecolor='#E91E63', linewidth=2)
        ax.add_patch(kafka_box)
        ax.text(9.75, 5, 'Apache Kafka', fontsize=11, fontweight='bold', ha='center')
        ax.text(9.75, 4.6, 'domain-events-oncall', fontsize=10, ha='center')
        ax.text(9.75, 4.3, '• Event Streaming', fontsize=9, ha='center')
        ax.text(9.75, 4.1, '• State Changes', fontsize=9, ha='center')
        
        # On-Call Specific Components
        oncall_components = FancyBboxPatch((1, 2), 10, 1.5, 
                                          boxstyle="round,pad=0.1", 
                                          facecolor='#FFF8E1', edgecolor='#F57F17', linewidth=2)
        ax.add_patch(oncall_components)
        ax.text(6, 3.2, 'On-Call Specific Components', fontsize=12, fontweight='bold', ha='center')
        ax.text(1.5, 2.8, 'Escalation Engine:', fontsize=10, fontweight='bold', ha='left')
        ax.text(2, 2.5, '• Policy-based escalation', fontsize=9, ha='left')
        ax.text(2, 2.2, '• Retry logic & timeouts', fontsize=9, ha='left')
        ax.text(5.5, 2.8, 'Responder Management:', fontsize=10, fontweight='bold', ha='left')
        ax.text(6, 2.5, '• UUID resolution to user info', fontsize=9, ha='left')
        ax.text(6, 2.2, '• Team & user lookups', fontsize=9, ha='left')
        ax.text(9, 2.8, 'Live Call Handling:', fontsize=10, fontweight='bold', ha='left')
        ax.text(9.5, 2.5, '• Phone integration', fontsize=9, ha='left')
        ax.text(9.5, 2.2, '• Call metadata', fontsize=9, ha='left')
        
        # Data Flow Arrows
        # API to Services
        arrow1 = FancyArrowPatch((6, 7.9), (6, 7.5),
                                arrowstyle='->', mutation_scale=20, color='#1976D2', linewidth=2)
        ax.add_patch(arrow1)
        
        # Services to PostgreSQL
        arrow2 = FancyArrowPatch((4, 6.2), (2.5, 5.3),
                                arrowstyle='<->', mutation_scale=20, color='#4CAF50', linewidth=2)
        ax.add_patch(arrow2)
        
        # Services to Elasticsearch
        arrow3 = FancyArrowPatch((6, 5.8), (6, 5.5),
                                arrowstyle='<->', mutation_scale=20, color='#FBC02D', linewidth=2)
        ax.add_patch(arrow3)
        
        # Services to Kafka
        arrow4 = FancyArrowPatch((8, 6.2), (9.5, 5.3),
                                arrowstyle='->', mutation_scale=20, color='#E91E63', linewidth=2)
        ax.add_patch(arrow4)
        
        # External to API
        arrow5 = FancyArrowPatch((6, 9.4), (6, 9.0),
                                arrowstyle='->', mutation_scale=20, color='#FF8F00', linewidth=2)
        ax.add_patch(arrow5)
        
        # On-Call Components to Services
        arrow6 = FancyArrowPatch((6, 3.6), (6, 5.8),
                                arrowstyle='<->', mutation_scale=20, color='#F57F17', linewidth=2)
        ax.add_patch(arrow6)
        
        # Configuration & Deployment Info
        config_box = FancyBboxPatch((1, 0.2), 10, 1.5, 
                                   boxstyle="round,pad=0.1", 
                                   facecolor='#F5F5F5', edgecolor='#757575', linewidth=1)
        ax.add_patch(config_box)
        ax.text(6, 1.4, 'Deployment Configuration', fontsize=11, fontweight='bold', ha='center')
        ax.text(1.5, 1.0, 'Environment Detection:', fontsize=10, fontweight='bold', ha='left')
        ax.text(2, 0.7, '• TENANT_NAME="on-call" environment variable', fontsize=9, ha='left')
        ax.text(2, 0.4, '• Automatic service routing and configuration', fontsize=9, ha='left')
        ax.text(6.5, 1.0, 'Multi-Region Deployment:', fontsize=10, fontweight='bold', ha='left')
        ax.text(7, 0.7, '• Independent per datacenter (us1, us3, us5, eu1, ap1, ap2)', fontsize=9, ha='left')
        ax.text(7, 0.4, '• Kubernetes values: config/k8s/values/tenants/on-call/', fontsize=9, ha='left')
        
        plt.tight_layout()
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return img_buffer

    def create_data_model_diagram(self):
        """Create a diagram showing on-call specific data models"""
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(7, 9.5, 'On-Call Data Model & Properties', 
                fontsize=16, fontweight='bold', ha='center')
        
        # Case/Page Entity
        case_box = FancyBboxPatch((1, 7), 5, 2, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor='#E3F2FD', edgecolor='#1976D2', linewidth=2)
        ax.add_patch(case_box)
        ax.text(3.5, 8.5, 'Case/Page Entity', fontsize=12, fontweight='bold', ha='center')
        ax.text(1.2, 8.2, '• work_type: PAGE (vs CASE)', fontsize=10, ha='left')
        ax.text(1.2, 7.9, '• status: TRIGGERED → ACKNOWLEDGED → RESOLVED', fontsize=10, ha='left')
        ax.text(1.2, 7.6, '• priority: Inherited from escalation policy', fontsize=10, ha='left')
        ax.text(1.2, 7.3, '• additional_properties.on_call: OnCallProperties', fontsize=10, ha='left')
        
        # OnCallProperties Structure
        oncall_props_box = FancyBboxPatch((8, 6.5), 5.5, 2.5, 
                                         boxstyle="round,pad=0.1", 
                                         facecolor='#FFF8E1', edgecolor='#F57F17', linewidth=2)
        ax.add_patch(oncall_props_box)
        ax.text(10.75, 8.7, 'OnCallProperties', fontsize=12, fontweight='bold', ha='center')
        ax.text(8.2, 8.4, '• escalation_policy_id: UUID', fontsize=9, ha='left')
        ax.text(8.2, 8.1, '• escalation_policy_step_id: UUID', fontsize=9, ha='left')
        ax.text(8.2, 7.8, '• escalation_policy_retry_count: int32', fontsize=9, ha='left')
        ax.text(8.2, 7.5, '• urgency: HIGH, NORMAL, LOW', fontsize=9, ha='left')
        ax.text(8.2, 7.2, '• responder_users: []ResponderUser', fontsize=9, ha='left')
        ax.text(8.2, 6.9, '• acknowledged_at: timestamp', fontsize=9, ha='left')
        ax.text(8.2, 6.6, '• time_to_first_acknowledge: duration', fontsize=9, ha='left')
        
        # ResponderUser Structure
        responder_box = FancyBboxPatch((1, 4.5), 5, 2, 
                                      boxstyle="round,pad=0.1", 
                                      facecolor='#E8F5E8', edgecolor='#4CAF50', linewidth=2)
        ax.add_patch(responder_box)
        ax.text(3.5, 6.2, 'ResponderUser', fontsize=12, fontweight='bold', ha='center')
        ax.text(1.2, 5.9, '• uuid: User UUID (PII filtered in ES)', fontsize=10, ha='left')
        ax.text(1.2, 5.6, '• name: "" (filtered out for privacy)', fontsize=10, ha='left')
        ax.text(1.2, 5.3, '• email: "" (filtered out for privacy)', fontsize=10, ha='left')
        ax.text(1.2, 5.0, '• resolved via UserService.GetUsersBatch()', fontsize=10, ha='left')
        ax.text(1.2, 4.7, '• used for faceted search & analytics', fontsize=10, ha='left')
        
        # Escalation Targets
        targets_box = FancyBboxPatch((8, 4), 5.5, 2, 
                                    boxstyle="round,pad=0.1", 
                                    facecolor='#F3E5F5', edgecolor='#9C27B0', linewidth=2)
        ax.add_patch(targets_box)
        ax.text(10.75, 5.7, 'EscalationTargets', fontsize=12, fontweight='bold', ha='center')
        ax.text(8.2, 5.4, '• teams: []EscalationTarget', fontsize=10, ha='left')
        ax.text(8.2, 5.1, '• users: []EscalationTarget', fontsize=10, ha='left')
        ax.text(8.2, 4.8, '• cross_org_handles: []string', fontsize=10, ha='left')
        ax.text(8.2, 4.5, '• used for routing and notifications', fontsize=10, ha='left')
        ax.text(8.2, 4.2, '• dynamic assignment based on queries', fontsize=10, ha='left')
        
        # Live Call Properties
        live_call_box = FancyBboxPatch((1, 2), 5, 2, 
                                      boxstyle="round,pad=0.1", 
                                      facecolor='#FCE4EC', edgecolor='#E91E63', linewidth=2)
        ax.add_patch(live_call_box)
        ax.text(3.5, 3.7, 'LiveCallProperties', fontsize=12, fontweight='bold', ha='center')
        ax.text(1.2, 3.4, '• integration_id: Phone integration UUID', fontsize=10, ha='left')
        ax.text(1.2, 3.1, '• live: boolean (active call status)', fontsize=10, ha='left')
        ax.text(1.2, 2.8, '• call_metadata: Call details & logs', fontsize=10, ha='left')
        ax.text(1.2, 2.5, '• phone_number: Caller information', fontsize=10, ha='left')
        ax.text(1.2, 2.2, '• duration: Call length tracking', fontsize=10, ha='left')
        
        # Special Features
        features_box = FancyBboxPatch((8, 1.5), 5.5, 2.5, 
                                     boxstyle="round,pad=0.1", 
                                     facecolor='#FFFDE7', edgecolor='#FBC02D', linewidth=2)
        ax.add_patch(features_box)
        ax.text(10.75, 3.7, 'Special Features', fontsize=12, fontweight='bold', ha='center')
        ax.text(8.2, 3.4, 'Event Deduplication:', fontsize=10, fontweight='bold', ha='left')
        ax.text(8.2, 3.1, '• event_deduplication_key: Prevents duplicates', fontsize=9, ha='left')
        ax.text(8.2, 2.8, 'Shadow Mode:', fontsize=10, fontweight='bold', ha='left')
        ax.text(8.2, 2.5, '• is_shadow: Testing without notifications', fontsize=9, ha='left')
        ax.text(8.2, 2.2, 'Auto-Assignment:', fontsize=10, fontweight='bold', ha='left')
        ax.text(8.2, 1.9, '• Query-based team assignment', fontsize=9, ha='left')
        ax.text(8.2, 1.6, '• Dynamic responder selection', fontsize=9, ha='left')
        
        # Relationships (arrows)
        # Case to OnCallProperties
        arrow1 = FancyArrowPatch((6.1, 8), (7.9, 8),
                                arrowstyle='->', mutation_scale=20, color='#F57F17', linewidth=2)
        ax.add_patch(arrow1)
        ax.text(7, 8.2, 'contains', fontsize=9, ha='center')
        
        # OnCallProperties to ResponderUser
        arrow2 = FancyArrowPatch((8.5, 6.4), (5.5, 5.8),
                                arrowstyle='->', mutation_scale=20, color='#4CAF50', linewidth=2)
        ax.add_patch(arrow2)
        ax.text(6.8, 6.2, 'references', fontsize=9, ha='center')
        
        # OnCallProperties to EscalationTargets
        arrow3 = FancyArrowPatch((10.75, 6.4), (10.75, 6.1),
                                arrowstyle='->', mutation_scale=20, color='#9C27B0', linewidth=2)
        ax.add_patch(arrow3)
        
        # Case to LiveCall
        arrow4 = FancyArrowPatch((3.5, 6.9), (3.5, 4.1),
                                arrowstyle='->', mutation_scale=20, color='#E91E63', linewidth=2)
        ax.add_patch(arrow4)
        ax.text(3.8, 5.5, 'includes', fontsize=9, ha='center')
        
        # Data Privacy & Security Note
        privacy_box = FancyBboxPatch((1, 0.2), 12.5, 0.8, 
                                    boxstyle="round,pad=0.05", 
                                    facecolor='#FFEBEE', edgecolor='#F44336', linewidth=1)
        ax.add_patch(privacy_box)
        ax.text(7.25, 0.6, 'Data Privacy & Security', fontsize=11, fontweight='bold', ha='center')
        ax.text(1.2, 0.3, 'PII Filtering: User names and emails are filtered out before ES indexing (see filterAdditionalProperties in case.go:139-150)', fontsize=9, ha='left')
        
        plt.tight_layout()
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return img_buffer

    def generate_report(self):
        """Generate the complete PDF report"""
        # Title Page
        self.content.append(Paragraph("On-Call Tenant Architecture Report", self.title_style))
        self.content.append(Paragraph("Case Management Domain - Complete Architecture Analysis", self.subheading_style))
        self.content.append(Spacer(1, 0.5 * inch))
        
        # Executive Summary
        self.content.append(Paragraph("Executive Summary", self.heading_style))
        summary_text = """
        This report provides a comprehensive analysis of the on-call tenant architecture within the case management domain. 
        The on-call tenant operates as a completely separate tenant from the main case management system, with its own 
        databases, Elasticsearch clusters, and service instances while sharing the same codebase through tenant-aware 
        business logic.

        Key architectural highlights include complete data isolation, independent scaling capabilities, separate failure 
        domains, and optimized configurations for on-call specific workflows including escalation policies, responder 
        management, and live call handling.
        """
        self.content.append(Paragraph(summary_text, self.body_style))
        self.content.append(Spacer(1, 0.3 * inch))
        
        # Table of Contents
        self.content.append(Paragraph("Table of Contents", self.heading_style))
        toc_data = [
            ["1. Tenant Architecture Overview", ""],
            ["2. Database Architecture", ""],
            ["3. Service Deployment Strategy", ""],
            ["4. On-Call Data Models", ""],
            ["5. Configuration Management", ""],
            ["6. Deployment Environments", ""],
            ["7. Security & Privacy", ""],
            ["8. Performance & Monitoring", ""],
            ["9. Integration Points", ""],
            ["10. Operational Considerations", ""]
        ]
        toc_table = Table(toc_data, colWidths=[4*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        self.content.append(toc_table)
        self.content.append(PageBreak())
        
        # Section 1: Tenant Architecture Overview
        self.content.append(Paragraph("1. Tenant Architecture Overview", self.heading_style))
        
        tenant_overview_text = """
        The case management domain implements a sophisticated multi-tenant architecture where the on-call tenant 
        operates completely independently from the main case management tenant. This separation ensures data isolation, 
        independent scaling, and specialized business logic optimized for on-call workflows.
        """
        self.content.append(Paragraph(tenant_overview_text, self.body_style))
        
        # Add tenant overview diagram
        tenant_diagram = self.create_tenant_overview_diagram()
        img = Image(tenant_diagram, width=7*inch, height=5*inch)
        self.content.append(img)
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Tenant Configuration Details
        self.content.append(Paragraph("Tenant Configuration", self.subheading_style))
        config_text = """
        Tenant configuration is managed through the tenants.yaml file which defines all tenant-specific settings:
        """
        self.content.append(Paragraph(config_text, self.body_style))
        
        config_code = """
        on-call:
          display_name: OnCall
          api_target: case-api-on-call.case-management.all-clusters.local-dc.fabric.dog:6481
          case_type: ON_CALL
          statuses:
            - ACKNOWLEDGED
            - RESOLVED  
            - TRIGGERED
          default_status: TRIGGERED
          final_status: RESOLVED
          work_type: PAGE
        """
        self.content.append(Paragraph(config_code, self.code_style))
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Key Differences Table
        self.content.append(Paragraph("Key Architectural Differences", self.subheading_style))
        diff_data = [
            ["Aspect", "Case Management", "On-Call"],
            ["Work Type", "CASE", "PAGE"],
            ["Default Status", "OPEN", "TRIGGERED"],
            ["Status Flow", "OPEN → IN_PROGRESS → CLOSED", "TRIGGERED → ACKNOWLEDGED → RESOLVED"],
            ["Database", "case-management", "case-management-oncall"],
            ["ES Cluster", "elasticsearch-casem-v8", "elasticsearch-casem-oncall"],
            ["Kafka Topic", "domain-events", "domain-events-oncall"],
            ["API Endpoint", "case-api.*", "case-api-on-call.*"],
            ["Service Focus", "General case tracking", "Incident response & escalation"],
        ]
        diff_table = Table(diff_data, colWidths=[1.5*inch, 2.25*inch, 2.25*inch])
        diff_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#E3F2FD')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#1976D2')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        self.content.append(diff_table)
        self.content.append(PageBreak())
        
        # Section 2: Database Architecture
        self.content.append(Paragraph("2. Database Architecture", self.heading_style))
        
        db_overview_text = """
        The on-call tenant maintains complete database separation from the case management tenant, ensuring data 
        isolation and independent scaling. Both staging and production environments follow the same architectural 
        patterns with environment-specific configurations.
        """
        self.content.append(Paragraph(db_overview_text, self.body_style))
        
        # Add database architecture diagram
        db_diagram = self.create_database_architecture_diagram()
        img = Image(db_diagram, width=7.5*inch, height=4.5*inch)
        self.content.append(img)
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Database Configuration Details
        self.content.append(Paragraph("Database Configuration Details", self.subheading_style))
        db_config_text = """
        Each tenant has its own PostgreSQL cluster with separate users, databases, and connection pools:
        """
        self.content.append(Paragraph(db_config_text, self.body_style))
        
        # Environment-specific database hosts
        env_db_data = [
            ["Environment", "Case Management Host", "On-Call Host"],
            ["Staging", "case-management-db.postgres.us1.staging.dog:5433", "case-management-oncall-db.postgres.us1.staging.dog:5433"],
            ["Production", "case-management-db.postgres.us1.prod.dog:5433", "case-management-oncall-db.postgres.us1.prod.dog:5433"],
        ]
        env_db_table = Table(env_db_data, colWidths=[1.5*inch, 2.75*inch, 2.75*inch])
        env_db_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#E8F5E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#2E7D32')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        self.content.append(env_db_table)
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Elasticsearch Configuration
        self.content.append(Paragraph("Elasticsearch Configuration", self.subheading_style))
        es_config_text = """
        Separate Elasticsearch clusters ensure search performance isolation and independent index management. 
        Both tenants use the same index name ('cases') but on completely separate clusters, allowing for 
        tenant-specific optimizations and scaling strategies.
        """
        self.content.append(Paragraph(es_config_text, self.body_style))
        
        es_clusters_data = [
            ["Tenant", "Cluster Name", "Index Name", "Purpose"],
            ["Case Management", "elasticsearch-casem-v8", "cases", "General case search & analytics"],
            ["On-Call", "elasticsearch-casem-oncall", "cases", "Page search & on-call analytics"],
        ]
        es_table = Table(es_clusters_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        es_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#FFFDE7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#F57F17')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
        ]))
        self.content.append(es_table)
        self.content.append(PageBreak())
        
        # Section 3: Service Architecture & Data Flow
        self.content.append(Paragraph("3. Service Architecture & Data Flow", self.heading_style))
        
        service_overview_text = """
        The on-call tenant follows the same service architecture patterns as the main case management tenant but 
        with dedicated service instances and specialized business logic for on-call workflows. This includes 
        escalation management, responder tracking, and integration with external notification systems.
        """
        self.content.append(Paragraph(service_overview_text, self.body_style))
        
        # Add service architecture diagram
        service_diagram = self.create_service_architecture_diagram()
        img = Image(service_diagram, width=7.5*inch, height=5.5*inch)
        self.content.append(img)
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Service Instances
        self.content.append(Paragraph("Service Instances", self.subheading_style))
        service_instances_text = """
        Each major service has dedicated on-call instances with specific routing and configuration:
        """
        self.content.append(Paragraph(service_instances_text, self.body_style))
        
        service_data = [
            ["Service Type", "Case Management", "On-Call"],
            ["API Service", "case-api.case-management.*", "case-api-on-call.case-management.*"],
            ["Event Relay", "case-event-relay.case-management.*", "case-event-relay-on-call.case-management.*"],
            ["Port", "6481", "6481"],
            ["Health Check", "/health", "/health"],
            ["Metrics", "/metrics", "/metrics"],
        ]
        service_table = Table(service_data, colWidths=[1.5*inch, 2.5*inch, 2.5*inch])
        service_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F3E5F5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#7B1FA2')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
        ]))
        self.content.append(service_table)
        self.content.append(PageBreak())
        
        # Section 4: On-Call Data Models
        self.content.append(Paragraph("4. On-Call Data Models", self.heading_style))
        
        data_model_text = """
        The on-call tenant utilizes specialized data structures optimized for incident response workflows. 
        These models extend the base case structure with on-call specific properties including escalation 
        policies, responder tracking, and live call metadata.
        """
        self.content.append(Paragraph(data_model_text, self.body_style))
        
        # Add data model diagram
        data_model_diagram = self.create_data_model_diagram()
        img = Image(data_model_diagram, width=7*inch, height=5*inch)
        self.content.append(img)
        self.content.append(Spacer(1, 0.2 * inch))
        
        # OnCallProperties Structure
        self.content.append(Paragraph("OnCallProperties Structure", self.subheading_style))
        oncall_props_text = """
        The OnCallProperties structure contains all on-call specific metadata and is stored in the 
        additional_properties.on_call field of each page:
        """
        self.content.append(Paragraph(oncall_props_text, self.body_style))
        
        oncall_props_code = """
        message OnCallProperties {
          string escalation_policy_id = 1;
          string escalation_policy_step_id = 2;
          int32 escalation_policy_retry_count = 3;
          Urgency urgency = 4;
          repeated ResponderUser responder_users = 5;
          google.protobuf.Timestamp acknowledged_at = 6;
          google.protobuf.Timestamp responders_added_at = 7;
          google.protobuf.Duration time_to_first_acknowledge = 8;
          LiveCallProperties live_call = 9;
          string event_deduplication_key = 10;
          bool is_shadow = 11;
          EscalationTargets targets = 12;
        }
        """
        self.content.append(Paragraph(oncall_props_code, self.code_style))
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Data Privacy Implementation
        self.content.append(Paragraph("Data Privacy Implementation", self.subheading_style))
        privacy_text = """
        User PII (names and emails) is filtered out before indexing in Elasticsearch to protect user privacy. 
        The filtering is implemented in the filterAdditionalProperties function:
        """
        self.content.append(Paragraph(privacy_text, self.body_style))
        
        privacy_code = """
        func filterAdditionalProperties(orgID uint64, additionalProperties *pb.AdditionalProperties) {
          if additionalProperties == nil {
            return
          }
          
          if additionalProperties.GetOnCall() != nil {
            for _, user := range additionalProperties.GetOnCall().GetResponderUsers() {
              user.Email = ""  // Remove PII
              user.Name = ""   // Remove PII
            }
          }
        }
        """
        self.content.append(Paragraph(privacy_code, self.code_style))
        self.content.append(PageBreak())
        
        # Section 5: Configuration Management
        self.content.append(Paragraph("5. Configuration Management", self.heading_style))
        
        config_mgmt_text = """
        Configuration management for the on-call tenant follows a hierarchical structure with environment-specific 
        overrides. The configuration is organized by tenant, datacenter, and environment to provide maximum 
        flexibility while maintaining consistency.
        """
        self.content.append(Paragraph(config_mgmt_text, self.body_style))
        
        # Configuration Structure
        self.content.append(Paragraph("Configuration Directory Structure", self.subheading_style))
        config_structure = """
        config/k8s/values/tenants/
        ├── case-management/
        │   ├── values.yaml                    # Base configuration
        │   └── datacenters/
        │       ├── us1/
        │       │   ├── staging.yaml          # US1 staging overrides
        │       │   └── prod.yaml             # US1 production overrides
        │       ├── us3/ ... (similar structure)
        │       └── eu1/ ... (similar structure)
        └── on-call/
            ├── values.yaml                    # Base on-call configuration
            └── datacenters/
                ├── us1/
                │   ├── staging.yaml          # US1 staging overrides
                │   └── prod.yaml             # US1 production overrides
                ├── us3/ ... (similar structure)
                └── eu1/ ... (similar structure)
        """
        self.content.append(Paragraph(config_structure, self.code_style))
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Tenant Detection Logic
        self.content.append(Paragraph("Tenant Detection Logic", self.subheading_style))
        tenant_detection_text = """
        The application determines which tenant configuration to use based on the TENANT_NAME environment variable:
        """
        self.content.append(Paragraph(tenant_detection_text, self.body_style))
        
        tenant_detection_code = """
        func GetCurrentTenantName() TenantName {
            tenantName := os.Getenv("TENANT_NAME")
            if tenantName == "" {
                return CaseManagementTenantName  // Default to case-management
            }
            return TenantName(tenantName)
        }

        func IsOnCallTenant() bool {
            return GetCurrentTenantName() == OnCallTenantName
        }

        func GetDefaultWorkType() pb.WorkType {
            if IsCaseManagementTenant() {
                return pb.WorkType_CASE
            }
            if IsOnCallTenant() {
                return pb.WorkType_PAGE
            }
            return pb.WorkType_UNKNOWN_WORK_TYPE
        }
        """
        self.content.append(Paragraph(tenant_detection_code, self.code_style))
        self.content.append(PageBreak())
        
        # Section 6: Deployment Environments
        self.content.append(Paragraph("6. Deployment Environments", self.heading_style))
        
        deployment_text = """
        The on-call tenant is deployed across multiple datacenters with environment-specific configurations 
        for both staging and production. Each deployment is completely independent, providing regional 
        isolation and disaster recovery capabilities.
        """
        self.content.append(Paragraph(deployment_text, self.body_style))
        
        # Datacenter Deployment Table
        self.content.append(Paragraph("Multi-Datacenter Deployment", self.subheading_style))
        dc_data = [
            ["Datacenter", "Region", "Staging Deployment", "Production Deployment"],
            ["us1", "US East", "✓ Full deployment", "✓ Full deployment"],
            ["us3", "US West", "✓ Full deployment", "✓ Full deployment"],
            ["us5", "US Central", "✓ Full deployment", "✓ Full deployment"],
            ["eu1", "Europe", "✓ Full deployment", "✓ Full deployment"],
            ["ap1", "Asia Pacific", "✓ Full deployment", "✓ Full deployment"],
            ["ap2", "Asia Pacific 2", "✓ Full deployment", "✓ Full deployment"],
        ]
        dc_table = Table(dc_data, colWidths=[1.2*inch, 1.3*inch, 1.75*inch, 1.75*inch])
        dc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#E8F5E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#2E7D32')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
        ]))
        self.content.append(dc_table)
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Deployment Strategy
        self.content.append(Paragraph("Deployment Strategy", self.subheading_style))
        deployment_strategy_text = """
        Each datacenter deployment includes:
        
        • Independent Kubernetes clusters with tenant-specific namespaces
        • Separate database instances with cross-datacenter replication
        • Region-specific Elasticsearch clusters for optimal search performance  
        • Local Kafka instances for event streaming with cross-region replication
        • Dedicated monitoring and alerting per region and tenant
        • Independent scaling policies based on regional traffic patterns
        """
        self.content.append(Paragraph(deployment_strategy_text, self.body_style))
        
        # Resource Allocation
        self.content.append(Paragraph("Resource Allocation", self.subheading_style))
        resource_data = [
            ["Component", "Staging Resources", "Production Resources"],
            ["API Pods", "2-4 replicas", "6-12 replicas"],
            ["Database", "Shared cluster", "Dedicated cluster"],
            ["Elasticsearch", "Shared nodes", "Dedicated nodes"],
            ["Memory Limits", "512Mi - 1Gi", "1Gi - 4Gi"],
            ["CPU Limits", "0.2 - 0.5 cores", "0.5 - 2 cores"],
            ["Storage", "Standard SSD", "Premium SSD + backups"],
        ]
        resource_table = Table(resource_data, colWidths=[1.5*inch, 2.25*inch, 2.25*inch])
        resource_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#FFF3E0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#E65100')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
        ]))
        self.content.append(resource_table)
        self.content.append(PageBreak())
        
        # Section 7: Security & Privacy
        self.content.append(Paragraph("7. Security & Privacy", self.heading_style))
        
        security_text = """
        The on-call tenant implements comprehensive security measures including data isolation, PII protection, 
        and secure communication protocols. Special attention is given to responder information privacy and 
        compliance with data protection regulations.
        """
        self.content.append(Paragraph(security_text, self.body_style))
        
        # Security Measures
        self.content.append(Paragraph("Security Measures", self.subheading_style))
        security_measures_text = """
        • **Data Isolation**: Complete separation of databases and search indexes
        • **PII Protection**: User names and emails filtered before Elasticsearch indexing
        • **Access Control**: Role-based access with tenant-specific permissions
        • **Encryption**: All data encrypted in transit (TLS) and at rest
        • **Audit Logging**: Comprehensive audit trails for all operations
        • **Network Security**: Private networking with VPC isolation
        • **Secret Management**: Kubernetes secrets with rotation policies
        • **Compliance**: SOC 2, GDPR, and HIPAA compliance measures
        """
        self.content.append(Paragraph(security_measures_text, self.body_style))
        
        # Privacy Implementation Details
        self.content.append(Paragraph("Privacy Implementation Details", self.subheading_style))
        privacy_details_text = """
        The system implements multiple layers of privacy protection specifically for on-call responder data:
        """
        self.content.append(Paragraph(privacy_details_text, self.body_style))
        
        privacy_layers_data = [
            ["Layer", "Implementation", "Purpose"],
            ["Storage Layer", "PII filtering before ES indexing", "Prevent sensitive data storage in search"],
            ["Access Layer", "UUID-based resolution", "Dynamic user info retrieval when needed"],
            ["API Layer", "Role-based field filtering", "Control what data is returned"],
            ["Transport Layer", "TLS encryption", "Secure data transmission"],
            ["Audit Layer", "Access logging", "Track who accessed what data"],
        ]
        privacy_table = Table(privacy_layers_data, colWidths=[1.3*inch, 2.35*inch, 2.35*inch])
        privacy_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#FFEBEE')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#C62828')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        self.content.append(privacy_table)
        self.content.append(PageBreak())
        
        # Section 8: Performance & Monitoring
        self.content.append(Paragraph("8. Performance & Monitoring", self.heading_style))
        
        performance_text = """
        The on-call tenant includes comprehensive monitoring and observability features with tenant-specific 
        metrics, alerting, and performance optimization strategies tailored for incident response workflows.
        """
        self.content.append(Paragraph(performance_text, self.body_style))
        
        # Monitoring Strategy
        self.content.append(Paragraph("Monitoring Strategy", self.subheading_style))
        monitoring_strategy_text = """
        • **Tenant-Specific Metrics**: Separate dashboards and metrics for each tenant
        • **SLA Tracking**: Independent SLA monitoring and reporting
        • **Performance Metrics**: Response time, throughput, and error rate tracking
        • **Business Metrics**: Time to acknowledge, escalation success rates
        • **Infrastructure Metrics**: Database performance, Elasticsearch query times
        • **Custom Alerting**: On-call specific alerting rules and escalation
        • **Distributed Tracing**: End-to-end request tracing across services
        • **Log Aggregation**: Structured logging with tenant identification
        """
        self.content.append(Paragraph(monitoring_strategy_text, self.body_style))
        
        # Key Performance Indicators
        self.content.append(Paragraph("Key Performance Indicators", self.subheading_style))
        kpi_data = [
            ["Metric Category", "Key Metrics", "Target"],
            ["Response Time", "API response time, Search query time", "< 500ms p95"],
            ["Availability", "Service uptime, Database availability", "> 99.9%"],
            ["Throughput", "Requests per second, Pages processed", "1000+ req/s"],
            ["On-Call Specific", "Time to acknowledge, Escalation success", "< 5 min, > 95%"],
            ["Error Rates", "4xx/5xx errors, Failed escalations", "< 1%"],
            ["Resource Usage", "CPU/Memory utilization, Storage growth", "< 80% avg"],
        ]
        kpi_table = Table(kpi_data, colWidths=[1.5*inch, 2.5*inch, 2*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#E8F5E8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#2E7D32')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        self.content.append(kpi_table)
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Performance Optimizations
        self.content.append(Paragraph("Performance Optimizations", self.subheading_style))
        optimizations_text = """
        The on-call tenant includes several performance optimizations specifically for incident response scenarios:
        
        • **SearchFacetValues Optimization**: Smart filter patterns and adaptive timeouts
        • **Elasticsearch Tuning**: Optimized shard sizing and execution hints
        • **Database Indexing**: Custom indexes for on-call query patterns
        • **Caching Strategies**: User resolution caching and query result caching
        • **Connection Pooling**: Optimized connection pools for high-frequency operations
        • **Async Processing**: Non-blocking escalation and notification processing
        """
        self.content.append(Paragraph(optimizations_text, self.body_style))
        self.content.append(PageBreak())
        
        # Section 9: Integration Points
        self.content.append(Paragraph("9. Integration Points", self.heading_style))
        
        integration_text = """
        The on-call tenant integrates with multiple external systems and services to provide comprehensive 
        incident response capabilities. These integrations are designed to be resilient and maintainable.
        """
        self.content.append(Paragraph(integration_text, self.body_style))
        
        # External Integrations
        self.content.append(Paragraph("External Integrations", self.subheading_style))
        integration_data = [
            ["Integration", "Purpose", "Protocol", "Endpoint"],
            ["Datadog On-Call API", "Page creation & management", "HTTPS/REST", "/api/unstable/on-call/pages"],
            ["User Service", "Responder info resolution", "gRPC", "Internal service mesh"],
            ["Project Service", "Access control & settings", "gRPC", "Internal service mesh"],
            ["Notification Service", "Email/SMS/Phone alerts", "HTTP/Webhook", "External notification providers"],
            ["Escalation Service", "Policy management", "gRPC", "Internal service mesh"],
            ["Analytics Service", "Metrics and reporting", "gRPC", "Internal analytics pipeline"],
        ]
        integration_table = Table(integration_data, colWidths=[1.4*inch, 1.8*inch, 1*inch, 1.8*inch])
        integration_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#F3E5F5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#7B1FA2')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        self.content.append(integration_table)
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Integration Architecture
        self.content.append(Paragraph("Integration Architecture Patterns", self.subheading_style))
        integration_patterns_text = """
        The on-call tenant uses several integration patterns to ensure reliability and maintainability:
        
        • **Circuit Breaker Pattern**: Protection against failing external services
        • **Retry with Backoff**: Resilient external API calls with exponential backoff
        • **Async Messaging**: Event-driven integration using Kafka topics
        • **Service Mesh**: Internal service-to-service communication via gRPC
        • **API Versioning**: Backward-compatible API evolution strategies
        • **Health Checks**: Continuous monitoring of integration health
        • **Fallback Mechanisms**: Graceful degradation when integrations fail
        """
        self.content.append(Paragraph(integration_patterns_text, self.body_style))
        self.content.append(PageBreak())
        
        # Section 10: Operational Considerations
        self.content.append(Paragraph("10. Operational Considerations", self.heading_style))
        
        operational_text = """
        Operating the on-call tenant requires specific operational procedures and considerations due to its 
        critical role in incident response. This section covers deployment procedures, troubleshooting, 
        and maintenance activities.
        """
        self.content.append(Paragraph(operational_text, self.body_style))
        
        # Deployment Procedures
        self.content.append(Paragraph("Deployment Procedures", self.subheading_style))
        deployment_procedures_text = """
        • **Blue-Green Deployment**: Zero-downtime deployments with traffic switching
        • **Canary Releases**: Gradual rollout with monitoring and rollback capabilities
        • **Database Migrations**: Coordinated schema changes across tenant databases
        • **Configuration Updates**: Hot-reload of tenant-specific configurations
        • **Rollback Procedures**: Quick rollback mechanisms for failed deployments
        • **Health Validation**: Automated health checks post-deployment
        """
        self.content.append(Paragraph(deployment_procedures_text, self.body_style))
        
        # Troubleshooting Guide
        self.content.append(Paragraph("Common Troubleshooting Scenarios", self.subheading_style))
        troubleshooting_data = [
            ["Issue", "Symptoms", "Resolution Steps"],
            ["Tenant Misconfiguration", "Wrong database connections", "Verify TENANT_NAME env var"],
            ["Search Timeouts", "SearchFacetValues failures", "Check ES cluster health, optimize queries"],
            ["User Resolution Failures", "Missing responder info", "Verify UserService connectivity"],
            ["Escalation Failures", "Pages not creating", "Check On-Call API integration"],
            ["Database Connection Issues", "Service startup failures", "Verify DB credentials and connectivity"],
            ["Cross-Tenant Data Leakage", "Wrong data in responses", "Verify tenant isolation filters"],
        ]
        troubleshooting_table = Table(troubleshooting_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
        troubleshooting_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#FFEBEE')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#C62828')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#CCCCCC')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        self.content.append(troubleshooting_table)
        self.content.append(Spacer(1, 0.2 * inch))
        
        # Maintenance Activities
        self.content.append(Paragraph("Routine Maintenance Activities", self.subheading_style))
        maintenance_text = """
        • **Database Maintenance**: Index rebuilding, statistics updates, backup verification
        • **Elasticsearch Maintenance**: Index optimization, cluster rebalancing, snapshot management
        • **Configuration Audits**: Regular review of tenant configurations and security settings
        • **Performance Tuning**: Query optimization, resource allocation adjustments
        • **Security Updates**: Regular security patches and vulnerability assessments
        • **Capacity Planning**: Monitoring growth trends and planning infrastructure scaling
        • **Disaster Recovery Testing**: Regular DR drills and recovery procedure validation
        """
        self.content.append(Paragraph(maintenance_text, self.body_style))
        
        # Conclusion
        self.content.append(Spacer(1, 0.3 * inch))
        self.content.append(Paragraph("Conclusion", self.heading_style))
        conclusion_text = """
        The on-call tenant architecture demonstrates a sophisticated approach to multi-tenancy that provides 
        complete isolation while maintaining operational efficiency. The architecture supports independent 
        scaling, specialized business logic, and comprehensive monitoring while sharing a common codebase.
        
        Key benefits of this architecture include:
        • Complete data and operational isolation between tenants
        • Independent scaling and performance optimization
        • Specialized business logic for on-call workflows
        • Comprehensive security and privacy protection
        • Resilient integration patterns with external systems
        • Operational excellence through monitoring and automation
        
        This architecture serves as a model for implementing multi-tenant systems that require both isolation 
        and specialized functionality while maintaining code reuse and operational efficiency.
        """
        self.content.append(Paragraph(conclusion_text, self.body_style))
        
        # Generate the PDF
        self.doc.build(self.content)
        print(f"On-Call Tenant Architecture Report generated: {self.pdf_path}")

if __name__ == "__main__":
    generator = OnCallTenantReportGenerator()
    generator.generate_report()