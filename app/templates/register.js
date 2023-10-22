const handleSubmit = (event) => {
    event.preventDefault();
  
    const myForm = event.target;
    const formData = new FormData(myForm);
    
    fetch("register", {
      credentials: 'include',
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(formData).toString(),
    })
    .then((response) =>{
      if (response.status == 409) {
        throw new Error("Already exist");
      }
      if (response.ok) {
        window.location.replace("/web/");
      }
    })
    .catch((err) => {
      document.getElementById("err").textContent=err;
      console.log(err);
    });
  };
  
  document
    .querySelector("form")
    .addEventListener("submit", handleSubmit);