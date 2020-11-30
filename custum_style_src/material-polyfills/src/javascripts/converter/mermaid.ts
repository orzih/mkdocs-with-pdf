// Convert from '.mermaid>svg' to embedded img

const isSVGSVGElement = (element: any): element is SVGSVGElement =>
  (element instanceof SVGSVGElement);

/*
const convertSVGto = (svgElement: SVGSVGElement) => {
  // Create canvas for converting image to data URL
  const image = document.createElement('img');
  const parent = svgElement.parentElement;

  const width = svgElement.clientWidth.toString() + 'px';
  const height = svgElement.clientWidth.toString() + 'px';

  image.setAttribute('width', width);
  image.setAttribute('height', height);

  svgElement.setAttribute('width', width);
  svgElement.setAttribute('height', width);

  const xml = new XMLSerializer().serializeToString(svgElement);
  const svg64 = btoa(unescape(encodeURIComponent(xml)));
  const image64 = 'data:image/svg+xml;base64,' + svg64;

  // Get data URL encoding of image
  image.setAttribute('src', image64);

  parent.replaceChild(image, svgElement);
}
*/

const convertSVGtoPng = (svgElement: SVGSVGElement) => {
  const scaleFactor = 400.0 / 96.0;  // 400 DPI
  const width = svgElement.clientWidth;
  const height = svgElement.clientHeight;
  const widthPx = width.toString() + 'px';
  const heightPx = height.toString() + 'px';

  const canvas = document.createElement('canvas');
  canvas.width = width * scaleFactor;
  canvas.height = height * scaleFactor;
  const context = canvas.getContext('2d');
  context.scale(scaleFactor, scaleFactor);

  const offscreen = new Image(width, height);
  offscreen.onload = () => {
    context.drawImage(offscreen, 0, 0, offscreen.width, offscreen.height);

    const image = document.createElement('img');
    const parent = svgElement.parentElement;

    image.setAttribute('src', canvas.toDataURL());
    image.setAttribute('width', widthPx);
    image.setAttribute('height', heightPx);

    parent.replaceChild(image, svgElement);
  }

  svgElement.setAttribute('width', widthPx);
  svgElement.setAttribute('height', heightPx);
  const xml = new XMLSerializer().serializeToString(svgElement);
  const svg64 = btoa(unescape(encodeURIComponent(xml)));
  const image64 = 'data:image/svg+xml;charset=utf-8;base64,' + svg64;
  offscreen.setAttribute('src', image64);
}

/**
 * NOTE: Set the `false` to `htmlLabels` option.
 *
 * WeasyPrint@52(CairoSVG) is not support `ForeignObject` in `svg`.
 *
 * @see https://github.com/Kozea/CairoSVG/issues/147
 */


interface Window { mermaid: any; }
if (window.mermaid) {
  window.mermaid.mermaidAPI.initialize({
    // flowchart: { htmlLabels: false },
    // htmlLabels: false,
    mermaid: {
      callback: (id) => {
        const svgElement = document.getElementById(id);
        if (!isSVGSVGElement(svgElement)) return;
        console.log('converting svg(' + id + ') to dataUri');
        // convertSVGto(svgElement);
        convertSVGtoPng(svgElement);
      }
    }
  })
}
