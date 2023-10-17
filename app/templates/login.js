
const postData = async (url = '') => {
  // Формируем запрос
  const response = await fetch(url, {
    // Метод, если не указывать, будет использоваться GET
    method: 'POST',
   // Заголовок запроса
    body: JSON.stringify({username: document.getElementById('login').value, password: document.getElementById('password').value}),
    headers: {
      'Content-Type': 'application/json'
    },
  }).then((responseJson) => {
    if(responseJson.status == 401){
      document.getElementById("err").textContent="Incorrect username or password";
    }
    if(responseJson.ok){
      window.location.href = responseJson.url;
    }
  }).catch((error) => {
    document.getElementById("err").textContent=res.json()["message"];
  });
  return response;
}

document.querySelector(".login-btn").addEventListener("click", (e)=>{
    postData('/token/'+ new URLSearchParams(new FormData(document.getElementById('form'))))
      }
    )