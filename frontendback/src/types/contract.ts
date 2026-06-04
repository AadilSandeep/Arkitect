export interface Goal {
    user_input: string;
    domain: string;
    goal_type: string;
    complexity: "Low" | "Medium" | "High";
  }
  
  export interface Deliverable {
    id: number;
    title: string;
    description: string;
  }
  
  export interface RecommendedTool {
    name: string;
    category: string;
    reason: string;
  }
  
  export interface WorkflowStep {
    step_number: number;
    title: string;
    tool: string;
    why: string;
    what_to_do: string;
    prompt: string;
    expected_result: string;
  }
  
  export interface AlternativeWorkflow {
    summary: string;
    tools: string[];
  }
  
  export interface AlternativeWorkflows {
    fastest: AlternativeWorkflow;
    cheapest: AlternativeWorkflow;
    highest_quality: AlternativeWorkflow;
    beginner_friendly: AlternativeWorkflow;
  }
  
  export interface KnowledgeAreas {
    high: string[];
    medium: string[];
    low: string[];
  }
  
  export interface WorkflowArchitectResponse {
    goal: Goal;
    deliverables: Deliverable[];
    recommended_tools: RecommendedTool[];
    workflow: WorkflowStep[];
    alternative_workflows: AlternativeWorkflows;
    knowledge_areas: KnowledgeAreas;
    estimated_time: string;
  }