const handleSubmit = (event) => {
  event.preventDefault();

  const myForm = event.target;
  const formData = new FormData(myForm);
  
  fetch("/token/", {
    credentials: 'include',
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams(formData).toString(),
  })
  .then((response) => response.json())
  .then((json) => {
    document.cookie = 'access_token=' + json['access_token'];
    document.cookie = 'token_type=' + json['token_type'];
  }).catch((err) => {
    console.log(err);
  });
};

document
  .querySelector("form")
  .addEventListener("submit", handleSubmit);