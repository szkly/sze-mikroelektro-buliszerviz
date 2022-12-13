document.addEventListener("DOMContentLoaded", async () => {
  await main();
});

const main = async () => {
  const { datasets, labels, names } = await getStats();

  await renderMultiLineChart(datasets, labels, names);
};

const renderMultiLineChart = async (datasets, labels, tooltipData) => {
  const chartConfig = generateChartConfig(datasets, labels, tooltipData);

  const chartCtx = document.querySelector("#chart-statistics");
  new Chart(chartCtx, chartConfig);
};

const generateChartConfig = (datasets, labels, tooltipData) => {
  const chartData = getChartData(datasets, labels);

  const config = {
    type: "line",
    data: chartData,
    options: {
      responsive: true,
      interaction: {
        mode: "index",
        intersect: true,
      },
      stacked: false,
      scales: {
        approvals: {
          type: "linear",
          display: true,
          position: "left",
        },
        denials: {
          type: "linear",
          display: true,
          position: "right",
          grid: {
            drawOnChartArea: false,
          },
        },
      },
      plugins: {
        tooltip: {
          callbacks: {
            footer: (context) => tooltipData[context[0].dataIndex],
          },
        },
      },
    },
  };

  return config;
};

const getChartData = (datasets, labels) => {
  const labelsNormalized = labels.map((label) => {
    return new Date(label).toLocaleString("hu");
  });

  const data = {
    labels: labelsNormalized,
    datasets: [
      {
        label: "Engedélyezett",
        data: datasets.approvals, // generating an array with the length corresponding to the number of approvals
        borderColor: "#2563EB",
        backgroundColor: "#2563EB",
        yAxisID: "approvals",
      },
      {
        label: "Megtagadott",
        data: datasets.denials, // generating an array with the length corresponding to the number of denials
        borderColor: "#CA8A04",
        backgroundColor: "#CA8A04",
        yAxisID: "denials",
      },
    ],
  };

  return data;
};

const getStats = async () => {
  const response = await fetch("/api/stats");

  return response.json();
};
