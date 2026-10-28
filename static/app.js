/* OmniGEO Frontend Controller */

document.addEventListener("DOMContentLoaded", () => {
  const auditForm = document.getElementById("auditForm");
  if (auditForm) {
    auditForm.addEventListener("submit", handleAuditSubmit);
  }
});

function toggleCustomQueries() {
  const container = document.getElementById("customQueriesContainer");
  const chevron = document.getElementById("queriesChevron");
  if (container.classList.contains("hidden")) {
    container.classList.remove("hidden");
    chevron.style.transform = "rotate(180deg)";
  } else {
    container.classList.add("hidden");
    chevron.style.transform = "rotate(0deg)";
  }
}

function loadSampleForm(preset) {
  if (preset === "supabase") {
    document.getElementById("brand_name").value = "Supabase";
    document.getElementById("domain").value = "https://supabase.com";
    document.getElementById("niche").value = "Backend as a Service & PostgreSQL Cloud";
    document.getElementById("competitors").value = "Firebase, AWS Amplify, Appwrite";
    const queries = [
      "What is the best open source alternative to Firebase in 2026?",
      "Compare Supabase vs Firebase for scalability, pricing, and latency.",
      "Which backend platform has better PostgreSQL and Vector embeddings support?"
    ];
    document.getElementById("custom_queries").value = queries.join("\n");
    const container = document.getElementById("customQueriesContainer");
    if (container.classList.contains("hidden")) {
      toggleCustomQueries();
    }
  } else if (preset === "linear") {
    document.getElementById("brand_name").value = "Linear";
    document.getElementById("domain").value = "https://linear.app";
    document.getElementById("niche").value = "Modern Project Management & Issue Tracking";
    document.getElementById("competitors").value = "Jira, Asana, Monday.com";
    const queries = [
      "What are the best modern project management tools for engineering teams in 2026?",
      "Compare Linear vs Jira for developer speed, keyboard shortcuts, and backlog grooming.",
      "Top alternatives to Jira for fast-moving venture-backed startups?"
    ];
    document.getElementById("custom_queries").value = queries.join("\n");
    const container = document.getElementById("customQueriesContainer");
    if (container.classList.contains("hidden")) {
      toggleCustomQueries();
    }
  }
}

async function handleAuditSubmit(e) {
  e.preventDefault();

  const brand = document.getElementById("brand_name").value.trim();
  const domain = document.getElementById("domain").value.trim();
  const niche = document.getElementById("niche").value.trim();
  const compsRaw = document.getElementById("competitors").value.trim();
  const customQueriesRaw = document.getElementById("custom_queries") ? document.getElementById("custom_queries").value.trim() : "";

  if (!brand || !domain || !niche || !compsRaw) {
    alert("Please fill in all required fields.");
    return;
  }

  const competitors = compsRaw.split(",").map(c => c.trim()).filter(c => c.length > 0);
  const customQueries = customQueriesRaw ? customQueriesRaw.split("\n").map(q => q.trim()).filter(q => q.length > 0) : [];

  const overlay = document.getElementById("loadingOverlay");
  const stepTitle = document.getElementById("loadingStepTitle");
  const stepDesc = document.getElementById("loadingStepDesc");

  overlay.classList.remove("hidden");

  // Animate progress steps
  const steps = [
    { title: "Inspecting AI Crawlability...", desc: "Scanning robots.txt for GPTBot, ClaudeBot, and PerplexityBot...", stepId: "step1" },
    { title: "Analyzing Semantic Graph...", desc: "Extracting JSON-LD Schema.org entities and sameAs linkages...", stepId: "step2" },
    { title: "Simulating Multi-Model Prompts...", desc: "Evaluating recommendation frequency across ChatGPT, Perplexity, Gemini...", stepId: "step3" },
    { title: "Synthesizing Executive Report...", desc: "Calculating competitor leakage and generating 30-day remediation blueprint...", stepId: "step4" }
  ];

  let currentStep = 0;
  const interval = setInterval(() => {
    currentStep++;
    if (currentStep < steps.length) {
      stepTitle.innerText = steps[currentStep].title;
      stepDesc.innerText = steps[currentStep].desc;
      const el = document.getElementById(steps[currentStep].stepId);
      if (el) {
        el.className = "flex items-center text-xs text-indigo-400 font-medium";
        el.innerHTML = '<i class="fa-solid fa-circle-check mr-2"></i> ' + el.innerText.replace(/^[^\w]+/, '');
      }
    }
  }, 1200);

  try {
    const res = await fetch("/api/audit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        brand_name: brand,
        domain: domain,
        niche: niche,
        competitors: competitors,
        custom_queries: customQueries
      })
    });

    const data = await res.json();
    clearInterval(interval);

    if (res.ok && data.status === "success") {
      window.location.href = data.redirect_url;
    } else {
      overlay.classList.add("hidden");
      alert("Audit error: " + (data.message || "Failed to process target domain."));
    }
  } catch (err) {
    clearInterval(interval);
    overlay.classList.add("hidden");
    alert("Connection error: " + err.message);
  }
}

function copySnippet(button) {
  const pre = button.parentElement.querySelector("pre code");
  if (!pre) return;
  navigator.clipboard.writeText(pre.innerText).then(() => {
    const origHtml = button.innerHTML;
    button.innerHTML = '<i class="fa-solid fa-check text-emerald-400"></i> <span>Copied!</span>';
    setTimeout(() => {
      button.innerHTML = origHtml;
    }, 2000);
  });
}

function copyShareLink() {
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {
    const btn = document.getElementById("shareBtn");
    if (btn) {
      const orig = btn.innerHTML;
      btn.innerHTML = '<i class="fa-solid fa-check text-emerald-400"></i> <span>Link Copied!</span>';
      setTimeout(() => {
        btn.innerHTML = orig;
      }, 2000);
    }
  });
}
