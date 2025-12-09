#!/usr/bin/env python3
"""
Case Management Search Architecture Diagram Generator
Generates comprehensive diagrams for the Case Management search system
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch, Arrow
import numpy as np

def create_search_architecture_diagram():
    """Creates the main search architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Color scheme
    colors = {
        'client': '#E8F4FD',
        'api': '#B8E6B8', 
        'handler': '#FFE5B4',
        'parser': '#FFCCCB',
        'elasticsearch': '#D8BFD8',
        'analytics': '#F0E68C',
        'enrichment': '#DDA0DD'
    }
    
    # Title
    ax.text(50, 95, 'Case Management Search Architecture', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Client Layer
    client_box = FancyBboxPatch((5, 85), 25, 8, boxstyle="round,pad=0.3", 
                               facecolor=colors['client'], edgecolor='black', linewidth=2)
    ax.add_patch(client_box)
    ax.text(17.5, 89, 'Search Clients\n(Web UI, API)', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # API Gateway Layer
    api_box = FancyBboxPatch((5, 73), 25, 8, boxstyle="round,pad=0.3", 
                            facecolor=colors['api'], edgecolor='black', linewidth=2)
    ax.add_patch(api_box)
    ax.text(17.5, 77, 'Case Rapid API\n/search endpoints', ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Query Handlers Layer
    search_handler = FancyBboxPatch((5, 58), 18, 10, boxstyle="round,pad=0.3", 
                                   facecolor=colors['handler'], edgecolor='black', linewidth=2)
    ax.add_patch(search_handler)
    ax.text(14, 63, 'SearchHandler\n• Basic Search\n• Pagination\n• Sorting', ha='center', va='center', fontsize=9)
    
    analytic_handler = FancyBboxPatch((27, 58), 18, 10, boxstyle="round,pad=0.3", 
                                     facecolor=colors['analytics'], edgecolor='black', linewidth=2)
    ax.add_patch(analytic_handler)
    ax.text(36, 63, 'AnalyticHandler\n• Time-series\n• Aggregations\n• Custom Attrs', ha='center', va='center', fontsize=9)
    
    facet_handler = FancyBboxPatch((49, 58), 18, 10, boxstyle="round,pad=0.3", 
                                  facecolor=colors['handler'], edgecolor='black', linewidth=2)
    ax.add_patch(facet_handler)
    ax.text(58, 63, 'FacetHandlers\n• Search Facets\n• Autocomplete\n• Get Attributes', ha='center', va='center', fontsize=9)
    
    # Query Parser Layer
    parser_box = FancyBboxPatch((5, 43), 62, 8, boxstyle="round,pad=0.3", 
                               facecolor=colors['parser'], edgecolor='black', linewidth=2)
    ax.add_patch(parser_box)
    ax.text(36, 47, 'Query Parser & Builder\n• ANTLR Grammar • ESQueryBuilder • Custom Attribute Support', 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Elasticsearch Layer
    es_box = FancyBboxPatch((5, 25), 62, 12, boxstyle="round,pad=0.3", 
                           facecolor=colors['elasticsearch'], edgecolor='black', linewidth=2)
    ax.add_patch(es_box)
    ax.text(36, 31, 'Elasticsearch Cluster\nMain Index: "cases"\nMapping: 393 fields including nested custom_attributes', 
            ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Index Structure Details
    ax.text(8, 28, 'Key Fields:\n• org_id, project_id\n• created_at, status\n• custom_attributes (nested)', 
            ha='left', va='center', fontsize=8)
    ax.text(45, 28, 'Analytics Fields:\n• analytics.status_*\n• date_range spans\n• metric calculations', 
            ha='left', va='center', fontsize=8)
    
    # Enrichment Services
    enrichment_box = FancyBboxPatch((75, 58), 20, 25, boxstyle="round,pad=0.3", 
                                   facecolor=colors['enrichment'], edgecolor='black', linewidth=2)
    ax.add_patch(enrichment_box)
    ax.text(85, 70.5, 'Enrichment Services\n\n• UserService (OUI)\n• ProjectService\n• CaseTypeService\n\nUUID → Names\nEmail Resolution\nProject Names', 
            ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Analytics Module Details
    analytics_detail = FancyBboxPatch((5, 5), 62, 15, boxstyle="round,pad=0.3", 
                                     facecolor=colors['analytics'], edgecolor='black', linewidth=1)
    ax.add_patch(analytics_detail)
    ax.text(36, 12.5, 'Analytics Module Integration', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(8, 9, '• Metrics: count, sum, avg, max, min, percentiles\n• GroupBy: 20+ fields + custom_attributes.*\n• Time Buckets: configurable intervals', 
            ha='left', va='center', fontsize=9)
    ax.text(8, 6, '• Nested Aggregations: custom attributes with reverse_nested\n• Runtime Fields: dynamic metric calculations', 
            ha='left', va='center', fontsize=9)
    
    # Arrows showing data flow
    # Client to API
    ax.arrow(17.5, 85, 0, -2, head_width=1, head_length=1, fc='black', ec='black')
    # API to Handlers
    ax.arrow(17.5, 73, 0, -3, head_width=1, head_length=1, fc='black', ec='black')
    ax.arrow(17.5, 70, 8.5, -7, head_width=1, head_length=1, fc='black', ec='black')
    ax.arrow(17.5, 70, 40.5, -7, head_width=1, head_length=1, fc='black', ec='black')
    # Handlers to Parser
    ax.arrow(36, 58, 0, -5, head_width=1, head_length=1, fc='black', ec='black')
    # Parser to ES
    ax.arrow(36, 43, 0, -4, head_width=1, head_length=1, fc='black', ec='black')
    # Enrichment connection
    ax.arrow(67, 63, 6, 0, head_width=1, head_length=1, fc='purple', ec='purple')
    
    plt.tight_layout()
    plt.savefig('/Users/agustin.fusaro/search_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_elasticsearch_mapping_diagram():
    """Creates detailed Elasticsearch mapping structure diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 95, 'Elasticsearch Index Structure: "cases"', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Core Fields Section
    core_box = FancyBboxPatch((5, 75), 40, 15, boxstyle="round,pad=0.5", 
                             facecolor='#E8F4FD', edgecolor='black', linewidth=2)
    ax.add_patch(core_box)
    ax.text(25, 87, 'Core Case Fields', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(7, 80, '• internal_id, case_id, public_id (keyword)\n• assignee_id, created_by (keyword)\n• project_id, org_id (keyword/long)\n• status, priority, type_id (long)\n• created_at, modified_at (date)\n• title, description (text)', 
            ha='left', va='center', fontsize=9)
    
    # Custom Attributes Section  
    custom_box = FancyBboxPatch((55, 75), 40, 15, boxstyle="round,pad=0.5", 
                               facecolor='#FFE5B4', edgecolor='black', linewidth=2)
    ax.add_patch(custom_box)
    ax.text(75, 87, 'Custom Attributes (Nested)', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(57, 80, '• Type: "nested" (not flattened object)\n• key (keyword) - attribute name\n• value_text (text) - string values\n• value_number (text + as_double) - numeric\n• Enables complex nested queries', 
            ha='left', va='center', fontsize=9)
    
    # Analytics Section
    analytics_box = FancyBboxPatch((5, 55), 40, 15, boxstyle="round,pad=0.5", 
                                  facecolor='#F0E68C', edgecolor='black', linewidth=2)
    ax.add_patch(analytics_box)
    ax.text(25, 67, 'Analytics Fields', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(7, 60, '• analytics.status_* (object)\n• spans (date_range) - time periods\n• total (long) - duration metrics\n• Supports time-based aggregations\n• Pre-computed metrics storage', 
            ha='left', va='center', fontsize=9)
    
    # Additional Properties Section
    additional_box = FancyBboxPatch((55, 55), 40, 15, boxstyle="round,pad=0.5", 
                                   facecolor='#D8BFD8', edgecolor='black', linewidth=2)
    ax.add_patch(additional_box)
    ax.text(75, 67, 'Additional Properties', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(57, 60, '• event_management.* - incident data\n• on_call.* - responder information\n• change_request.* - CR metadata\n• campaign.* - campaign data\n• Flattened structure for easy querying', 
            ha='left', va='center', fontsize=9)
    
    # Attributes Section
    attr_box = FancyBboxPatch((5, 35), 40, 15, boxstyle="round,pad=0.5", 
                             facecolor='#B8E6B8', edgecolor='black', linewidth=2)
    ax.add_patch(attr_box)
    ax.text(25, 47, 'Standard Attributes', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(7, 40, '• attributes (flattened) - key-value pairs\n• service, team, version, datacenter\n• rule_id, follow_up_incident_public_id\n• Used for faceted search and filtering\n• Direct field access for performance', 
            ha='left', va='center', fontsize=9)
    
    # Integration Fields Section
    integration_box = FancyBboxPatch((55, 35), 40, 15, boxstyle="round,pad=0.5", 
                                    facecolor='#FFCCCB', edgecolor='black', linewidth=2)
    ax.add_patch(integration_box)
    ax.text(75, 47, 'Integration Fields', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(57, 40, '• jira_issue.* - Jira integration\n• servicenow_ticket.* - ServiceNow\n• insights.* - ML insights\n• notification_handles.* - alerting\n• External system synchronization', 
            ha='left', va='center', fontsize=9)
    
    # Mapping Statistics
    stats_box = FancyBboxPatch((5, 15), 90, 15, boxstyle="round,pad=0.5", 
                              facecolor='#F5F5F5', edgecolor='black', linewidth=2)
    ax.add_patch(stats_box)
    ax.text(50, 27, 'Index Mapping Statistics', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(7, 20, '• Total Properties: 393+ fields\n• Dynamic Mapping: false (explicit schema)\n• Nested Objects: custom_attributes\n• Flattened Objects: attributes, additional_properties', 
            ha='left', va='center', fontsize=10)
    ax.text(55, 20, '• Text Fields: title, description (full-text search)\n• Keyword Fields: IDs, status enums (exact match)\n• Date Fields: timestamps with time-based queries\n• Long Fields: counters, enums, numeric identifiers', 
            ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('/Users/agustin.fusaro/elasticsearch_mapping.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_query_flow_diagram():
    """Creates the query processing flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 95, 'Search Query Processing Flow', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Step boxes
    steps = [
        ('Input Query', 'status:open AND priority:high', 85, '#E8F4FD'),
        ('ANTLR Parsing', 'Lexical analysis\nSyntax tree generation', 73, '#FFCCCB'),
        ('ES Query Building', 'Convert to Elasticsearch DSL\nAdd org/project filters', 61, '#FFE5B4'),
        ('Query Execution', 'Send to ES cluster\nApply aggregations/sorting', 49, '#D8BFD8'),
        ('Result Processing', 'Extract hits/aggregations\nConvert ES docs to protobuf', 37, '#B8E6B8'),
        ('Enrichment', 'Resolve UUIDs to names\nAdd user/project details', 25, '#DDA0DD'),
        ('Response', 'Return paginated results\nWith metadata', 13, '#F0E68C')
    ]
    
    for i, (title, desc, y, color) in enumerate(steps):
        box = FancyBboxPatch((10, y-4), 80, 8, boxstyle="round,pad=0.5", 
                            facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(15, y, title, ha='left', va='center', fontsize=12, fontweight='bold')
        ax.text(15, y-2, desc, ha='left', va='center', fontsize=9)
        
        # Arrow to next step
        if i < len(steps) - 1:
            ax.arrow(50, y-4, 0, -4, head_width=2, head_length=1, fc='black', ec='black')
    
    plt.tight_layout()
    plt.savefig('/Users/agustin.fusaro/query_flow.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_analytics_aggregation_diagram():
    """Creates analytics aggregation structure diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 95, 'Analytics Aggregation Architecture', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Root Aggregation
    root_box = FancyBboxPatch((35, 85), 30, 8, boxstyle="round,pad=0.3", 
                             facecolor='#F0E68C', edgecolor='black', linewidth=2)
    ax.add_patch(root_box)
    ax.text(50, 89, 'Root Aggregation', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Group By Options
    normal_group = FancyBboxPatch((5, 68), 35, 12, boxstyle="round,pad=0.3", 
                                 facecolor='#B8E6B8', edgecolor='black', linewidth=2)
    ax.add_patch(normal_group)
    ax.text(22.5, 76, 'Standard GroupBy', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(22.5, 71, 'Terms/MultiTerms Aggregation\n• assignee, status, priority\n• project, service, team\n• Single/Multiple fields', 
            ha='center', va='center', fontsize=9)
    
    custom_group = FancyBboxPatch((60, 68), 35, 12, boxstyle="round,pad=0.3", 
                                 facecolor='#FFE5B4', edgecolor='black', linewidth=2)
    ax.add_patch(custom_group)
    ax.text(77.5, 76, 'Custom Attributes GroupBy', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(77.5, 71, 'Nested Aggregation Structure\n• custom_attributes.key filter\n• text_values + number_values\n• reverse_nested for time buckets', 
            ha='center', va='center', fontsize=9)
    
    # Time Buckets
    time_box = FancyBboxPatch((35, 48), 30, 12, boxstyle="round,pad=0.3", 
                             facecolor='#D8BFD8', edgecolor='black', linewidth=2)
    ax.add_patch(time_box)
    ax.text(50, 56, 'Time Bucket Aggregation', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(50, 51, 'DateRange Aggregation\n• Configurable intervals\n• 1s to 1year buckets\n• Max 1000 buckets limit', 
            ha='center', va='center', fontsize=9)
    
    # Metrics
    metrics_box = FancyBboxPatch((35, 28), 30, 12, boxstyle="round,pad=0.3", 
                                facecolor='#FFCCCB', edgecolor='black', linewidth=2)
    ax.add_patch(metrics_box)
    ax.text(50, 36, 'Metric Aggregation', ha='center', va='center', fontsize=11, fontweight='bold')
    ax.text(50, 31, 'count, sum, avg, max, min\npercentiles (pc50, pc95, pc99)\nRuntime field calculations', 
            ha='center', va='center', fontsize=9)
    
    # Custom Attribute Detail
    detail_box = FancyBboxPatch((5, 5), 90, 18, boxstyle="round,pad=0.5", 
                               facecolor='#F5F5F5', edgecolor='black', linewidth=2)
    ax.add_patch(detail_box)
    ax.text(50, 20, 'Custom Attribute Aggregation Details', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(7, 12, 'Structure: nested → filter → terms → reverse_nested → date_range → metric\n\n1. Nested: Enter custom_attributes array\n2. Filter: Match specific attribute key (e.g., "environment")\n3. Terms: Group by text_values.keyword or number_values.as_double\n4. Reverse_nested: Exit to parent document for time calculations\n5. Date_range: Create time buckets\n6. Metric: Apply aggregation method (count, avg, etc.)', 
            ha='left', va='center', fontsize=10)
    
    # Arrows
    ax.arrow(50, 85, -20, -10, head_width=1.5, head_length=1.5, fc='blue', ec='blue')
    ax.arrow(50, 85, 20, -10, head_width=1.5, head_length=1.5, fc='orange', ec='orange')
    ax.arrow(22.5, 68, 15, -10, head_width=1.5, head_length=1.5, fc='blue', ec='blue')
    ax.arrow(77.5, 68, -15, -10, head_width=1.5, head_length=1.5, fc='orange', ec='orange')
    ax.arrow(50, 48, 0, -6, head_width=1.5, head_length=1.5, fc='black', ec='black')
    
    plt.tight_layout()
    plt.savefig('/Users/agustin.fusaro/analytics_aggregation.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Generating Case Management Search Architecture Diagrams...")
    
    create_search_architecture_diagram()
    print("✓ Created search_architecture.png")
    
    create_elasticsearch_mapping_diagram()
    print("✓ Created elasticsearch_mapping.png")
    
    create_query_flow_diagram()
    print("✓ Created query_flow.png")
    
    create_analytics_aggregation_diagram()
    print("✓ Created analytics_aggregation.png")
    
    print("\nAll diagrams generated successfully!")