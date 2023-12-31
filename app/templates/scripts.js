
const postData = async (url = '', data = {}) => {
  // Формируем запрос
  const response = await fetch(url, {
    // Метод, если не указывать, будет использоваться GET
    method: 'POST',
   // Заголовок запроса
    headers: {
      'Content-Type': 'application/json'
    },
    // Данные
    body: JSON.stringify(data)
  });
  return response.json();
}

function like(id){
    postData('/web/like/'+id)
      .then((data) => {
        console.log(data);
      });
}

function dislike(id){
    postData('/web/dislike/'+id)
      .then((data) => {
        console.log(data);
      });
}

function dell(id){
    postData('/web/dellPost/'+id)
      .then((data) => {
        console.log(data);
      });
}

document.querySelectorAll(".btn-like").forEach(el => {
    el.addEventListener("click", (e)=>{
        if (e.currentTarget.classList.contains('active')){
            dislike(e.currentTarget.getAttribute("data-id"))
            e.currentTarget.lastChild.data = parseInt(e.currentTarget.lastChild.data) - 1
        }
        else{
            like(e.currentTarget.getAttribute("data-id"))
            e.currentTarget.lastChild.data = parseInt(e.currentTarget.lastChild.data) + 1
        }
     e.currentTarget.classList.toggle('active');
    })
})

document.querySelectorAll(".btn-dell").forEach(el => {
    el.addEventListener("click", (e)=>{
        dell(e.currentTarget.getAttribute("data-id"));
        e.currentTarget.parentElement.parentElement.parentElement.classList.add("visually-hidden");
        var o = true;
    })
})


function logout() {
  document.cookie = "access_token= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
  document.cookie = "token_type= ; expires = Thu, 01 Jan 1970 00:00:00 GMT";
  window.location.replace("/web/posts");
}
