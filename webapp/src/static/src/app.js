document.addEventListener("DOMContentLoaded", () => {
  main();
});

const main = () => {
  const nameInput = document.querySelector("#input-name");
  const sendBtn = document.querySelector("#btn-send");

  nameInput.addEventListener("input", () => {
    const name = nameInput.value;

    sendBtn.disabled = name.length == 0;
  });

  sendBtn.addEventListener("click", async () => {
    const name = nameInput.value;

    const response = await sendName(name);
    showMessage(response);

    nameInput.value = "";
  });
};

const sendName = async (name) => {
  const requestBody = { name };

  const response = await fetch("/api/send-name", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  return response.json();
};

const showMessage = (response) => {
  console.log(response);

  bgColor = response.status == "success" ? "bg-emerald-800" : "bg-red-800";
  textColor = "text-white";

  messageBox = document.querySelector("#message-box");

  messageBox.classList.add(bgColor, textColor);
  messageBox.textContent = response.message;

  messageBox.classList.remove("hidden");

  setTimeout(() => {
    messageBox.classList.add("hidden");
    messageBox.classList.remove(bgColor, textColor);
  }, 3000);
};
