import { type FormEvent, useMemo, useState } from "react";
import { acceptOffer, createApplication, submitApplication } from "./api";
import type { ApplicationPayload, ApplicationStatus, CreditApplication } from "./types";

const demoData: ApplicationPayload = {
  product_code: "WORKING_CAPITAL",
  company_name: "ООО «Будущее дело»",
  inn: "7707083893",
  requested_amount: 2_000_000,
  term_months: 12,
  purpose: "Закупка товара",
  annual_revenue: 18_000_000,
  monthly_debt_payments: 120_000,
  years_in_business: 4,
  has_overdue_debt: false,
  contact_name: "Анна Иванова",
  contact_email: "demo@example.ru",
};

const statusLabels: Record<ApplicationStatus, string> = {
  DRAFT: "Черновик",
  SUBMITTED: "Отправлена",
  VALIDATING: "Проверка данных",
  SCORING: "Скоринг",
  NEEDS_INFORMATION: "Нужны данные",
  MANUAL_REVIEW: "Ручная проверка",
  OFFERED: "Оффер готов",
  ACCEPTED: "Условия приняты",
  DECLINED: "Отказ",
  CANCELLED: "Отменена",
};

const money = new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 0 });

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
    </label>
  );
}

export default function App() {
  const [form, setForm] = useState<ApplicationPayload>(demoData);
  const [application, setApplication] = useState<CreditApplication | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const progress = useMemo(() => {
    if (!application) return 20;
    if (["OFFERED", "ACCEPTED", "DECLINED", "MANUAL_REVIEW"].includes(application.status)) return 100;
    return 55;
  }, [application]);

  const set = <K extends keyof ApplicationPayload>(key: K, value: ApplicationPayload[K]) =>
    setForm((current) => ({ ...current, [key]: value }));

  async function startFlow(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const draft = await createApplication(form);
      setApplication(draft);
      const result = await submitApplication(draft.id);
      setApplication(result);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Неизвестная ошибка");
    } finally {
      setLoading(false);
    }
  }

  async function accept() {
    if (!application) return;
    setLoading(true);
    setError(null);
    try {
      setApplication(await acceptOffer(application.id));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Неизвестная ошибка");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Альфа Бизнес">
          <span className="brand-mark">A</span>
          <span>Альфа Бизнес</span>
        </a>
        <span className="prototype-badge">Прототип · тестовые данные</span>
      </header>

      <main id="top">
        <section className="hero">
          <div>
            <p className="eyebrow">Кредит для бизнеса</p>
            <h1>От заявки до решения<br />за несколько минут</h1>
            <p className="hero-copy">Ответьте на вопросы о бизнесе. Мы покажем каждый этап и объясним результат.</p>
          </div>
          <div className="hero-card">
            <span>Доступно</span>
            <strong>до 30 млн ₽</strong>
            <small>на срок до 36 месяцев</small>
          </div>
        </section>

        <section className="workspace">
          <div className="main-column">
            <div className="steps" aria-label="Прогресс заявки">
              <div className="steps-track"><span style={{ width: `${progress}%` }} /></div>
              <div><strong>1</strong><span>Анкета</span></div>
              <div className={application ? "active" : ""}><strong>2</strong><span>Проверка</span></div>
              <div className={progress === 100 ? "active" : ""}><strong>3</strong><span>Решение</span></div>
            </div>

            {!application ? (
              <form className="panel form-panel" onSubmit={startFlow}>
                <div className="panel-heading">
                  <div><p className="eyebrow">Шаг 1 из 3</p><h2>Расскажите о бизнесе</h2></div>
                  <button type="button" className="text-button" onClick={() => setForm(demoData)}>Заполнить демо</button>
                </div>
                <div className="form-grid">
                  <Field label="Кредитный продукт"><select value={form.product_code} onChange={(e) => set("product_code", e.target.value)}><option value="WORKING_CAPITAL">На оборотные средства</option></select></Field>
                  <Field label="Название компании"><input required minLength={2} value={form.company_name} onChange={(e) => set("company_name", e.target.value)} /></Field>
                  <Field label="ИНН"><input required pattern="[0-9]{10}|[0-9]{12}" value={form.inn} onChange={(e) => set("inn", e.target.value)} /></Field>
                  <Field label="Сумма, ₽"><input required type="number" min={100000} max={30000000} step={10000} value={form.requested_amount} onChange={(e) => set("requested_amount", Number(e.target.value))} /></Field>
                  <Field label="Срок, месяцев"><input required type="number" min={3} max={36} value={form.term_months} onChange={(e) => set("term_months", Number(e.target.value))} /></Field>
                  <Field label="Цель"><select value={form.purpose} onChange={(e) => set("purpose", e.target.value)}><option>Закупка товара</option><option>Покупка оборудования</option><option>Кассовый разрыв</option></select></Field>
                  <Field label="Годовая выручка, ₽"><input required type="number" min={1} value={form.annual_revenue} onChange={(e) => set("annual_revenue", Number(e.target.value))} /></Field>
                  <Field label="Платежи по долгам в месяц, ₽"><input required type="number" min={0} value={form.monthly_debt_payments} onChange={(e) => set("monthly_debt_payments", Number(e.target.value))} /></Field>
                  <Field label="Сколько лет работает бизнес"><input required type="number" min={0} value={form.years_in_business} onChange={(e) => set("years_in_business", Number(e.target.value))} /></Field>
                  <Field label="Контактное лицо"><input required value={form.contact_name} onChange={(e) => set("contact_name", e.target.value)} /></Field>
                  <Field label="Email"><input required type="email" value={form.contact_email} onChange={(e) => set("contact_email", e.target.value)} /></Field>
                  <label className="checkbox-field"><input type="checkbox" checked={form.has_overdue_debt} onChange={(e) => set("has_overdue_debt", e.target.checked)} /><span>Есть текущая просрочка</span></label>
                </div>
                {error && <div className="error" role="alert">{error}</div>}
                <div className="form-footer"><p>Нажимая кнопку, вы запускаете демо-проверку.</p><button className="primary" disabled={loading}>{loading ? "Проверяем…" : "Получить решение"}</button></div>
              </form>
            ) : (
              <section className={`panel result-panel status-${application.status.toLowerCase()}`}>
                <p className="eyebrow">Заявка № {application.id.slice(0, 8).toUpperCase()}</p>
                <h2>{statusLabels[application.status]}</h2>
                <p className="decision-copy">{application.decision_reason ?? "Заявка сохранена."}</p>
                {application.status === "OFFERED" && (
                  <div className="offer">
                    <div><span>Сумма</span><strong>{money.format(Number(application.approved_amount))} ₽</strong></div>
                    <div><span>Срок</span><strong>{application.approved_term_months} мес.</strong></div>
                    <div><span>Ставка</span><strong>{application.annual_rate}%</strong></div>
                  </div>
                )}
                {application.risk_score !== null && <p className="score-note">Индикатор риска MVP: <strong>{application.risk_score}/100</strong>. Это демо-оценка, а не реальное решение банка.</p>}
                {error && <div className="error" role="alert">{error}</div>}
                <div className="result-actions">
                  {application.status === "OFFERED" && <button className="primary" onClick={accept} disabled={loading}>Принять условия</button>}
                  <button className="secondary" onClick={() => { setApplication(null); setError(null); }}>Новая заявка</button>
                </div>
              </section>
            )}
          </div>

          <aside className="panel timeline-panel">
            <p className="eyebrow">Процесс</p>
            <h3>Что происходит с заявкой</h3>
            {application ? (
              <ol className="timeline">
                {application.status_history.map((event) => (
                  <li key={event.id}><span className="dot" /><div><strong>{statusLabels[event.to_status]}</strong><p>{event.reason}</p><small>{event.actor}</small></div></li>
                ))}
              </ol>
            ) : (
              <ol className="preview-list">
                <li><strong>1. Проверим анкету</strong><span>Формат данных и полноту</span></li>
                <li><strong>2. Оценим риск</strong><span>Покажем, что влияет на решение</span></li>
                <li><strong>3. Дадим результат</strong><span>Оффер, ручная проверка или отказ</span></li>
              </ol>
            )}
          </aside>
        </section>
      </main>
    </div>
  );
}

