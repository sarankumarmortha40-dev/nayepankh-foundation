const hamburger = document.querySelector(".hamburger");

hamburger.addEventListener("click", () => {
    alert("Mobile menu will be connected in the next version.");
});

///
// script.js

const stats = [
  {
    value: "1200+",
    title: "Total Volunteers"
  },
  {
    value: "350+",
    title: "Events Conducted"
  },
  {
    value: "50K+",
    title: "Beneficiaries Reached"
  },
  {
    value: "80+",
    title: "Partner Organizations"
  }
];

const statsContainer = document.getElementById("stats-grid");

stats.forEach(stat => {
  statsContainer.innerHTML += `
    <div class="stat-card">
      <h3>${stat.value}</h3>
      <p>${stat.title}</p>
    </div>
  `;
});