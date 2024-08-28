document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("runSecurityScript")
    .addEventListener("click", function () {
      // Send a POST request to the Flask route
      fetch("/run_security_script", { method: "POST" })
        .then((response) => {
          if (response.ok) {
            console.log("Security script is running...");
          } else {
            console.error("Failed to run security script");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
});
