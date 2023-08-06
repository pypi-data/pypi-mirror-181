function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function addHTMLtext(image_path, name, post, description) {
  var html_text = `
  <div class="image">
      <img src="{image_path}" class="profile-img">
  </div>
  <div class="content">
      <h1 class="title">Olá, me chamo <mark class="name">{name}</mark> <br>e sou <mark class="post">{post}</mark>.</h2>
      <p class="description" id="description">{description}</p>
      <button class="button" id="saiba_mais" onclick="handleClick(this)">Saiba mais</button>
  </div>
  `;
  html_text = html_text.replace("{image_path}", image_path);
  html_text = html_text.replace("{name}", name);
  html_text = html_text.replace("{post}", post);
  html_text = html_text.replace("{description}", description);
  
  document.querySelector('.center').insertAdjacentHTML(
    'afterbegin',
    html_text     
  )
}

function handleClick(component){
  sendValue(component.id);
}

var first_run = true;

function onRender(event) {
  if (first_run) {
    var {image_path, name, post, description} = event.detail.args;

    addHTMLtext(image_path, name, post, description);

    first_run = false;
  }

  if (!window.rendered) {
    window.rendered = true
  }
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(300)
Streamlit.setFrameWidth(704)
