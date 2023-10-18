
document.getElementById('form').addEventListener("submit", (e) => {
  let form = document.getElementById('form');
  form.action = '/token/';
  form.method = 'POST';
});

const postData = async (url = '') => {
  let form = document.getElementById('form');
  form.action = '/token/';
  form.method = 'POST';
  // form.innerHTML += '<input name="grant_type" value="password">';
  form.submit();

  // let formData = new FormData();
  // formData.append('grant_type', 'password');
  // formData.append('username', document.getElementById('username').value);
  // formData.append('password', document.getElementById('password').value);

  // form.formData
  // // Формируем запрос
  // const response = await fetch(url, {
  //   // Метод, если не указывать, будет использоваться GET
  //   method: 'POST',
  //   // redirect: 'follow',
  //  // Заголовок запроса
  //   // body: new URLSearchParams(formData),
  //   body: new URLSearchParams (formData),
  //   headers: {
  //     'Accept': 'application/json, text/plain, */*',
  //     'Content-Type': 'application/json'
  //   },
  // }).then((responseJson) => {
  //   if(responseJson.status == 401){
  //     document.getElementById("err").textContent="Incorrect username or password";
  //   }
  //   if(responseJson.ok){
  //     window.location.href = responseJson.url;
  //   }
  // }).catch((error) => {
  //   document.getElementById("err").textContent=res.json()["message"];
  // });
  // return response;
}

document.querySelector(".login-btn").addEventListener("click", (e)=>{
    postData('/token/')
      }
    )