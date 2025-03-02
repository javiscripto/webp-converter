document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("qualityImput").oninput = function() {
    const displayValue = document.getElementById("qualityValue");
    displayValue.innerHTML = this.value;
  };
  // const form = document.getElementById("upload-form");
  // form.addEventListener("submit", async (e) => {
  //   e.preventDefault();
  //   //obtener el archivo
  //   const file = document.getElementById("fileInput").files[0];
  //   const allowedFiles = ["png", "jpg", "jpeg"];
  //   if (!allowedFiles.includes(file.name.split(".").pop().toLowerCase())) {
  //     alert("formato no permitido");
  //     return;
  //   }
  // });
});
