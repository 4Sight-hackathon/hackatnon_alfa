export type ApplicationStatus =
  | "DRAFT"
  | "SUBMITTED"
  | "VALIDATING"
  | "SCORING"
  | "NEEDS_INFORMATION"
  | "MANUAL_REVIEW"
  | "OFFERED"
  | "ACCEPTED"
  | "DECLINED"
  | "CANCELLED";

export interface ApplicationPayload {
  product_code: string;
  company_name: string;
  inn: string;
  requested_amount: number;
  term_months: number;
  purpose: string;
  annual_revenue: number;
  monthly_debt_payments: number;
  years_in_business: number;
  has_overdue_debt: boolean;
  contact_name: string;
  contact_email: string;
}

export interface StatusEvent {
  id: string;
  from_status: ApplicationStatus | null;
  to_status: ApplicationStatus;
  actor: string;
  reason: string;
  created_at: string;
}

export interface CreditApplication extends ApplicationPayload {
  id: string;
  status: ApplicationStatus;
  risk_score: number | null;
  decision_reason: string | null;
  approved_amount: string | null;
  approved_term_months: number | null;
  annual_rate: string | null;
  created_at: string;
  updated_at: string;
  status_history: StatusEvent[];
}

