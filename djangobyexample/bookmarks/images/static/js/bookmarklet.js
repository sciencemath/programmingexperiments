const SITE_URL = '//127.0.0.1:8000/'
const STYLE_URL = SITE_URL + 'static/css/bookmarklet.css'
const MIN_WIDTH = 250
const MIN_HEIGHT = 250

const [head] = document.getElementsByTagName('head')
const link = document.createElement('link')
link.rel = 'stylesheet'
link.type = 'text/css'
link.href = STYLE_URL + '?r=' + Math.floor(Math.random()*99999999)
head.appendChild(link)

const [body] = document.getElementsByTagName('body')
body.innerHTML = `
  <div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Select an image to bookmark:</h1>
    <div class="images"></div>
  </div>
` + body.innerHTML

const bookmarkletLaunch = () => {
  const bookmarklet = document.getElementById('bookmarklet')
  const imagesFound = bookmarklet.querySelector('.images')

  imagesFound.innerHTML = ''
  bookmarklet.style.display = 'block'

  bookmarklet.querySelector('#close')
    .addEventListener('click', () => bookmarklet.style.display = 'none')

  const images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]')
  console.log('images', images)
  images.forEach(image => {
    if (image.naturalWidth >= MIN_WIDTH && image.naturalHeight >= MIN_HEIGHT) {
      const imageFound = document.createElement('img')
      imageFound.src = image.src
      imagesFound.append(imageFound)
    }
  })
}

bookmarkletLaunch()