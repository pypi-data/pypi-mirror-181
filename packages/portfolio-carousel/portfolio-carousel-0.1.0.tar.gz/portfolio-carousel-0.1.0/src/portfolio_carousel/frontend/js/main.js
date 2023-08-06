function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function addHead2HTML(title, subtitle) {
  var html_text = `
  <h1 class="carousel-title">{title}</h2>
  <p class="carousel-description">{subtitle}</o>
  `;
  html_text = html_text.replace("{title}", title);
  html_text = html_text.replace("{subtitle}", subtitle);
  
  document.querySelector('.slide-container').insertAdjacentHTML(
    'afterbegin',
    html_text     
  )
}

function addCards2HTML(card_image_path, card_title, card_keys, card_description, card_id) {
  var html_text = `
  <div class="card swiper-slide">
    <div class="image">
        <img src="{card_image_path}" class="card-img">
    </div>
    
    <div class="content">
        <h2 class="title">{card_title}</h2>
        <p class="keys">{card_keys}</p>
        <p class="description" id="description">{card_description}</p>
        <button class="button" id="{card_id}" onclick="handleClick(this)">👁 View More</button>
    </div>
  </div>
  `;
  html_text = html_text.replace("{card_image_path}", card_image_path);
  html_text = html_text.replace("{card_title}", card_title);
  html_text = html_text.replace("{card_keys}", card_keys);
  html_text = html_text.replace("{card_description}", card_description);
  html_text = html_text.replace("{card_id}", card_id);

  document.querySelector('.card-wrapper').insertAdjacentHTML(
    'beforeend',
    html_text     
  )
}

function handleClick(component){
  sendValue(component.id);
}


var first_run = true;

function onRender(event) {
  if (first_run) {
    var {title, subtitle, cards} = event.detail.args;

    addHead2HTML(title, subtitle);

    for (var i=0 ; i < cards.length ; i++){
      addCards2HTML(cards[i][0], cards[i][1], cards[i][2], cards[i][3], cards[i][1].toLowerCase().replaceAll(" ", "_"));
    }

    first_run = false;
  }


  if (!window.rendered) {
    window.rendered = true
  }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(700)
Streamlit.setFrameWidth(704)
