// Convert from '.twemoji>svg' to embedded img

const twemojiConverter = () => {
  const entries = document.querySelectorAll('.twemoji>svg')
  if (!entries || entries.length == 0) return
  entries.forEach((svgElement) => {
    const imgElement = document.createElement('img')

    const styles = window.getComputedStyle(svgElement)
    const fillColor = styles.color || '#333'

    svgElement.setAttribute('style', `fill:${fillColor};`)

    //imgElement.setAttribute('style', `width:${styles.width};height:${styles.height};`)
    //imgElement.setAttribute('style', `width:1.125rem;height:auto;`)

    const serializedSVG = new XMLSerializer().serializeToString(svgElement)
    const src = 'data:image/svg+xml;base64,' + window.btoa(serializedSVG)
    imgElement.setAttribute('src', src)

    svgElement.parentNode.replaceChild(imgElement, svgElement)
  })
}

twemojiConverter()
