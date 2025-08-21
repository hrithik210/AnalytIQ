// API configuration and service functions
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export interface AnalysisResult {
  report_id: string;
  storyteller_output: {
    narrative_report?: string;
    executive_summary?: string;
    key_insights?: string[];
    recommendations?: string[];
  };
  chart_data: Array<{
    chart_type: string;
    data: any;
    layout: any;
    title: string;
  }>;
}

export interface UploadResponse {
  report_id: string;
  storyteller_output: any;
  chart_data: any[];
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return await response.json();
  }

  async uploadAndAnalyze(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseUrl}/api/v1/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Upload failed with status ${response.status}`);
    }

    return await response.json();
  }

  async analyzeSupabaseCSV(bucket: string, path: string): Promise<UploadResponse> {
    const response = await fetch(`${this.baseUrl}/api/v1/analyze-supabase`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bucket, path })
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Analyze failed with status ${response.status}`);
    }
    return await response.json();
  }

  // Future endpoints can be added here
  async getReportById(reportId: string): Promise<AnalysisResult> {
    const response = await fetch(`${this.baseUrl}/api/v1/reports/${reportId}`);
    if (!response.ok) {
      throw new Error(`Failed to get report: ${response.status}`);
    }
    return await response.json();
  }
}

export const apiService = new ApiService();
