// Chem-E-Consultant Dashboard: Fully Interactive & Professional
// All logic in vanilla JS, no frameworks

document.addEventListener('DOMContentLoaded', () => {
  ChemEDashboard.init();
});

const ChemEDashboard = {
  events: [],
  orchestratorLog: [],
  alerts: [],
  assets: [
    { id: 1, name: 'Turbine #1', status: 'Healthy', risk: 'Low', trend: '+2%' },
    { id: 2, name: 'Pipeline A', status: 'At Risk', risk: 'Medium', trend: '-1%' },
    { id: 3, name: 'Turbine #3', status: 'Critical', risk: 'High', trend: '-5%' }
  ],
  compliance: 92,
  cost: 1.23,
  costUnit: 'M',
  training: [
    { name: 'Alice', status: 'Complete', expires: '2025-01-10' },
    { name: 'Bob', status: 'Expiring', expires: '2024-07-01' },
    { name: 'Carlos', status: 'Expired', expires: '2024-04-01' }
  ],
  aiInsights: [
    'Optimize turbine #3 maintenance schedule',
    'Reduce inspection cycle for pipeline A',
    'Update training for new EPA rule',
    'Consolidate vendor onboarding',
    'Review asset tag rounding policy'
  ],
  monthlyReviews: [],
  benefitsInfo: {
    'Dashboards': 'Legacy: Multiple dashboards in different systems. New: All-in-one view.',
    'Decision Gates': 'Legacy: Many manual gates. New: One AI-powered gate.',
    'Average Alert Routing': 'Legacy: Slow, manual routing. New: Instant, AI-driven.',
    'Report Prep Time': 'Legacy: Manual, slow. New: Automated, fast.',
    'Data Silos': 'Legacy: Data scattered. New: Unified cloud hub.'
  },
  alertTypes: {
    'Critical Safety': { class: 'alert-critical', timing: 0, auto: 'Shutdown command issued', urgency: 60 },
    'Compliance Drift': { class: 'alert-compliance', timing: 3600, auto: 'Draft gap report generated', urgency: 3600 },
    'Asset Failure Risk': { class: 'alert-asset', timing: 900, auto: 'Maintenance task scheduled', urgency: 900 },
    'Rounding': { class: 'alert-rounding', timing: 14400, auto: 'Small alert & data adjust', urgency: 14400 },
    'Training Lapse': { class: 'alert-training', timing: 86400, auto: 'Auto-assign micro-course', urgency: 86400 }
  },
  init() {
    this.renderEventForm();
    this.renderEventLog();
    this.renderOrchestratorLog();
    this.renderAlertMatrix();
    this.renderDashboard();
    this.renderDocumentation();
    this.renderBenefitsTable();
    this.setupModals();
    this.setupToasts();
  },
  // --- Entry Points ---
  renderEventForm() {
    const form = document.getElementById('event-form');
    form.onsubmit = (e) => {
      e.preventDefault();
      const type = document.getElementById('event-type').value;
      const details = document.getElementById('event-details').value.trim();
      if (!type || !details) return;
      const event = {
        id: Date.now(),
        type,
        details,
        time: new Date(),
        status: 'Pending'
      };
      this.events.unshift(event);
      this.renderEventLog();
      this.openOrchestratorModal(event);
      form.reset();
    };
  },
  renderEventLog() {
    const log = document.getElementById('event-log');
    log.innerHTML = this.events.length === 0 ? '<em>No events yet.</em>' :
      this.events.slice(0, 10).map(ev =>
        `<div class="event"><strong>${ev.type}</strong> - ${ev.details} <span style="color:#888;font-size:0.9em;">(${this.timeAgo(ev.time)})</span><br><span>Status: ${ev.status}</span></div>`
      ).join('');
  },
  // --- Orchestrator ---
  renderOrchestratorLog() {
    const log = document.getElementById('orchestrator-log');
    log.innerHTML = this.orchestratorLog.length === 0 ? '<em>No orchestrator decisions yet.</em>' :
      this.orchestratorLog.slice(0, 10).map(entry =>
        `<div class="orchestrator-entry"><strong>${entry.event.type}</strong> - ${entry.event.details}<br>
        <span>Answers: ${entry.answers.map(a => a ? 'Yes' : 'No').join(', ')}</span><br>
        <span>Outcome: <span style="color:${entry.color}">${entry.outcome}</span></span></div>`
      ).join('');
  },
  openOrchestratorModal(event) {
    const questions = [
      'Safety impact?',
      'Compliance deviation?',
      'Asset health risk level?',
      'Budget variance?',
      'Training or policy gap?'
    ];
    let answers = [false, false, false, false, false];
    let html = `<h3>Orchestrator Decision</h3><p>Event: <strong>${event.type}</strong> - ${event.details}</p><form id="orchestrator-form">`;
    questions.forEach((q, i) => {
      html += `<div style="margin-bottom:0.5em;"><label>${q}</label>
        <input type="radio" name="q${i}" value="yes" id="q${i}y" required><label for="q${i}y">Yes</label>
        <input type="radio" name="q${i}" value="no" id="q${i}n"><label for="q${i}n">No</label></div>`;
    });
    html += `<button type="submit" class="btn">Submit</button></form>`;
    this.showModal(html);
    document.getElementById('orchestrator-form').onsubmit = (e) => {
      e.preventDefault();
      answers = questions.map((_, i) => document.querySelector(`input[name='q${i}']:checked`).value === 'yes');
      let outcome, color, alertType;
      if (answers[0]) { outcome = 'Escalate'; color = '#ff4d4f'; alertType = 'Critical Safety'; }
      else if (answers[1] || answers[2]) { outcome = 'Schedule Task'; color = '#faad14'; alertType = answers[2] ? 'Asset Failure Risk' : 'Compliance Drift'; }
      else { outcome = 'Auto-Resolve'; color = '#52c41a'; alertType = 'Rounding'; }
      this.orchestratorLog.unshift({ event, answers, outcome, color });
      event.status = outcome;
      this.renderOrchestratorLog();
      this.renderEventLog();
      this.addAlert(alertType, event);
      this.showModal(`<h3>Outcome: <span style='color:${color}'>${outcome}</span></h3><p>Event routed as <strong>${outcome}</strong>.</p><button class='btn' id='close-modal-btn'>Close</button>`);
      document.getElementById('close-modal-btn').onclick = () => this.hideModal();
      this.showToast(`Event processed: ${outcome}`);
    };
  },
  // --- Alerts ---
  addAlert(type, event) {
    const alertDef = this.alertTypes[type];
    const id = Date.now() + Math.random();
    const alert = {
      id,
      type,
      class: alertDef.class,
      auto: alertDef.auto,
      event,
      created: Date.now(),
      urgency: alertDef.urgency,
      dismissed: false
    };
    this.alerts.unshift(alert);
    this.renderAlertMatrix();
    this.startAlertTimer(alert);
  },
  renderAlertMatrix() {
    const list = document.getElementById('alert-list');
    if (!list) return;
    list.innerHTML = this.alerts.filter(a => !a.dismissed).slice(0, 5).map(a =>
      `<div class="alert ${a.class}" tabindex="0" aria-label="${a.type}" data-id="${a.id}">
        <span><strong>${a.type}</strong> &mdash; ${a.auto}</span>
        <span class="timer" id="timer-${a.id}">${this.formatUrgency(a)}</span>
        <button class="btn" style="margin-left:1em;" onclick="ChemEDashboard.dismissAlert(${a.id})">Dismiss</button>
      </div>`
    ).join('');
  },
  startAlertTimer(alert) {
    if (alert.timer) clearInterval(alert.timer);
    alert.timer = setInterval(() => {
      const el = document.getElementById('timer-' + alert.id);
      if (!el) { clearInterval(alert.timer); return; }
      alert.urgency--;
      el.textContent = this.formatUrgency(alert);
      if (alert.urgency <= 0) {
        this.dismissAlert(alert.id);
        this.showToast(`${alert.type} auto-dismissed.`);
        clearInterval(alert.timer);
      }
    }, 1000);
  },
  dismissAlert(id) {
    const alert = this.alerts.find(a => a.id === id);
    if (alert) {
      alert.dismissed = true;
      this.renderAlertMatrix();
    }
  },
  formatUrgency(alert) {
    if (alert.urgency > 3600) return Math.ceil(alert.urgency/3600) + 'h';
    if (alert.urgency > 60) return Math.ceil(alert.urgency/60) + 'm';
    return alert.urgency + 's';
  },
  // --- Dashboard ---
  renderDashboard() {
    // Asset Map
    const assetMap = document.getElementById('asset-map');
    assetMap.innerHTML = `<h3>Live Asset Map</h3><svg width="100%" height="80" viewBox="0 0 300 80">${this.assets.map((a,i) =>
      `<circle cx="${50+i*100}" cy="40" r="25" fill="${a.status==='Healthy'?'#52c41a':a.status==='At Risk'?'#faad14':'#ff4d4f'}" data-asset="${a.id}" style="cursor:pointer;" tabindex="0" />
      <text x="${50+i*100}" y="80" text-anchor="middle" font-size="12">${a.name}</text>`).join('')}</svg><p>Click asset for details.</p>`;
    assetMap.querySelectorAll('circle').forEach(c => {
      c.onclick = () => this.openAssetModal(c.getAttribute('data-asset'));
      c.onkeydown = (e) => { if (e.key==='Enter') this.openAssetModal(c.getAttribute('data-asset')); };
    });
    // Compliance Gauge
    const gauge = document.getElementById('compliance-gauge');
    gauge.innerHTML = `<h3>Compliance Gauge</h3><div style="height:60px;display:flex;align-items:center;">
      <div style="width:80%;background:#e6f7ff;border-radius:8px;overflow:hidden;">
        <div id="gauge-bar" style="width:${this.compliance}%;background:#52c41a;height:24px;transition:width 0.7s;"></div>
      </div>
      <span style="margin-left:1rem;font-weight:bold;">${this.compliance}%</span>
    </div><p>Real-time compliance history</p>`;
    // Cost Dial
    const costDial = document.getElementById('cost-dial');
    costDial.innerHTML = `<h3>Cost vs. Budget</h3><svg width="100" height="60">
      <circle cx="50" cy="50" r="40" fill="#f0f0f0" />
      <path id="cost-arc" d="${this.describeArc(50,50,40,0,Math.min(360,this.cost/2*360))}" fill="#faad14" />
      <text x="50" y="55" text-anchor="middle" font-size="18" font-weight="bold">$${this.cost.toFixed(2)}${this.costUnit}</text>
    </svg><p>Auto-rounded to 5 sig figs</p><button class="btn" id="simulate-cost">Simulate Cost Update</button>`;
    document.getElementById('simulate-cost').onclick = () => {
      this.cost = +(Math.random()*2+0.5).toFixed(2);
      this.renderDashboard();
      this.showToast('Cost updated!');
    };
    // Training Status
    const training = document.getElementById('training-status');
    training.innerHTML = `<h3>Training Status</h3><ul>${this.training.map((t,i) =>
      `<li>${t.name} - <span style="color:${t.status==='Complete'?'#52c41a':t.status==='Expiring'?'#faad14':'#ff4d4f'}">${t.status}</span> (expires: ${t.expires}) <button class="btn" style="font-size:0.9em;" onclick="ChemEDashboard.toggleTraining(${i})">Toggle</button></li>`).join('')}</ul>`;
    // AI Insights
    const ai = document.getElementById('ai-insights');
    ai.innerHTML = `<h3>AI Insights</h3><ol>${this.aiInsights.map(i=>`<li>${i}</li>`).join('')}</ol><p><em>From monthly review</em></p><button class="btn" id="regen-insights">Regenerate Insights</button>`;
    document.getElementById('regen-insights').onclick = () => {
      this.aiInsights = this.generateInsights();
      this.renderDashboard();
      this.showToast('AI Insights regenerated!');
      this.addMonthlyReview();
    };
  },
  openAssetModal(assetId) {
    const asset = this.assets.find(a => a.id == assetId);
    if (!asset) return;
    this.showModal(`<h3>${asset.name}</h3><p>Status: <strong>${asset.status}</strong></p><p>Risk: <strong>${asset.risk}</strong></p><p>Weekly trend: <strong>${asset.trend}</strong></p><button class='btn' id='close-modal-btn'>Close</button>`);
    document.getElementById('close-modal-btn').onclick = () => this.hideModal();
  },
  toggleTraining(i) {
    const t = this.training[i];
    if (t.status === 'Complete') t.status = 'Expiring';
    else if (t.status === 'Expiring') t.status = 'Expired';
    else t.status = 'Complete';
    this.renderDashboard();
    this.showToast('Training status updated!');
  },
  generateInsights() {
    const pool = [
      'Optimize turbine #3 maintenance schedule',
      'Reduce inspection cycle for pipeline A',
      'Update training for new EPA rule',
      'Consolidate vendor onboarding',
      'Review asset tag rounding policy',
      'Increase compliance audit frequency',
      'Automate cost reporting',
      'Upgrade IoT sensor firmware',
      'Expand micro-course library',
      'Integrate new regulatory feed'
    ];
    return Array.from({length:5},()=>pool[Math.floor(Math.random()*pool.length)]);
  },
  describeArc(cx, cy, r, startAngle, endAngle) {
    // SVG arc for cost dial
    const start = this.polarToCartesian(cx, cy, r, endAngle);
    const end = this.polarToCartesian(cx, cy, r, startAngle);
    const largeArcFlag = endAngle - startAngle <= 180 ? '0' : '1';
    return [
      'M', cx, cy,
      'L', start.x, start.y,
      'A', r, r, 0, largeArcFlag, 0, end.x, end.y,
      'Z'
    ].join(' ');
  },
  polarToCartesian(cx, cy, r, angle) {
    const rad = (angle-90)*Math.PI/180.0;
    return { x: cx + (r * Math.cos(rad)), y: cy + (r * Math.sin(rad)) };
  },
  // --- Documentation & Reporting ---
  renderDocumentation() {
    const form = document.getElementById('doc-upload-form');
    const preview = document.getElementById('doc-preview');
    form.onsubmit = (e) => {
      e.preventDefault();
      const file = document.getElementById('doc-photo').files[0];
      if (!file) { this.showToast('Please select a photo.'); return; }
      const reader = new FileReader();
      reader.onload = (ev) => {
        preview.innerHTML = `<img src="${ev.target.result}" alt="Inspection Photo" /><p>Auto-tagged to asset: <strong>${this.assets[Math.floor(Math.random()*this.assets.length)].name}</strong></p>`;
        this.showToast('Photo auto-tagged and attached!');
      };
      reader.readAsDataURL(file);
      form.reset();
    };
    document.getElementById('generate-report').onclick = () => {
      // PDF generation using jsPDF
      if (typeof window.jspdf === 'undefined' && typeof window.jsPDF === 'undefined') {
        this.showToast('jsPDF library not loaded!');
        return;
      }
      const doc = new (window.jspdf ? window.jspdf.jsPDF : window.jsPDF)();
      doc.setFontSize(18);
      doc.text('Compliance Report', 14, 20);
      doc.setFontSize(12);
      let y = 32;
      doc.text('Recent Events:', 14, y);
      y += 8;
      this.events.slice(0,5).forEach(e => {
        doc.text(`- ${e.type}: ${e.details} (${e.status})`, 16, y);
        y += 7;
      });
      y += 4;
      doc.text(`Compliance: ${this.compliance}%`, 14, y);
      y += 8;
      doc.text(`Cost: $${this.cost.toFixed(2)}${this.costUnit}`, 14, y);
      doc.save('compliance_report.pdf');
      this.showToast('Compliance report PDF generated!');
    };
    this.renderMonthlyReviewLog();
    document.getElementById('documentation-panel').innerHTML = `
      <ul>
        <li><strong>Auto-Labeling:</strong> Inspection photos tagged to assets</li>
        <li><strong>Compliance Docs:</strong> Forms filled from inspection data</li>
        <li><strong>Monthly Review:</strong> AI emails key trends (5 sig figs) + actions</li>
      </ul>
    `;
  },
  addMonthlyReview() {
    const review = {
      date: new Date(),
      insights: this.aiInsights.slice()
    };
    this.monthlyReviews.unshift(review);
    this.renderMonthlyReviewLog();
  },
  renderMonthlyReviewLog() {
    const log = document.getElementById('monthly-review-log');
    if (!log) return;
    log.innerHTML = this.monthlyReviews.length === 0 ? '' :
      `<strong>Monthly Reviews Sent:</strong><ul>${this.monthlyReviews.slice(0,3).map(r=>`<li>${r.date.toLocaleString()}: <em>${r.insights.join('; ')}</em></li>`).join('')}</ul>`;
  },
  // --- Benefits Table ---
  renderBenefitsTable() {
    const info = this.benefitsInfo;
    document.getElementById('benefits-table').innerHTML = `
      <table>
        <tr><th>Area</th><th>Legacy Workflow</th><th>New Workflow</th></tr>
        <tr><td>Dashboards <span class="benefit-info" tabindex="0">&#9432;<span class="tooltip">${info['Dashboards']}</span></span></td><td>5+ separate</td><td>1 unified</td></tr>
        <tr><td>Decision Gates <span class="benefit-info" tabindex="0">&#9432;<span class="tooltip">${info['Decision Gates']}</span></span></td><td>5+</td><td>1</td></tr>
        <tr><td>Average Alert Routing <span class="benefit-info" tabindex="0">&#9432;<span class="tooltip">${info['Average Alert Routing']}</span></span></td><td>15 min–1 hour</td><td>&lt; 1 min</td></tr>
        <tr><td>Report Prep Time <span class="benefit-info" tabindex="0">&#9432;<span class="tooltip">${info['Report Prep Time']}</span></span></td><td>2–3 days</td><td>&lt; 5 min</td></tr>
        <tr><td>Data Silos <span class="benefit-info" tabindex="0">&#9432;<span class="tooltip">${info['Data Silos']}</span></span></td><td>4+ systems</td><td>0 (cloud hub)</td></tr>
      </table>
    `;
  },
  // --- Modals & Toasts ---
  setupModals() {
    const overlay = document.getElementById('modal-overlay');
    const closeBtn = document.getElementById('modal-close');
    closeBtn.onclick = () => this.hideModal();
    overlay.onclick = (e) => { if (e.target === overlay) this.hideModal(); };
    document.addEventListener('keydown', (e) => {
      if (!overlay.classList.contains('hidden') && e.key === 'Escape') this.hideModal();
    });
  },
  showModal(html) {
    const overlay = document.getElementById('modal-overlay');
    document.getElementById('modal-content').innerHTML = html;
    overlay.classList.remove('hidden');
    overlay.focus();
  },
  hideModal() {
    document.getElementById('modal-overlay').classList.add('hidden');
  },
  setupToasts() {
    this.toastContainer = document.getElementById('toast-container');
  },
  showToast(msg) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = msg;
    this.toastContainer.appendChild(toast);
    setTimeout(() => { toast.remove(); }, 3000);
  },
  // --- Utils ---
  timeAgo(date) {
    const now = new Date();
    const diff = Math.floor((now - new Date(date))/1000);
    if (diff < 60) return diff + 's ago';
    if (diff < 3600) return Math.floor(diff/60) + 'm ago';
    if (diff < 86400) return Math.floor(diff/3600) + 'h ago';
    return Math.floor(diff/86400) + 'd ago';
  }
}; 
