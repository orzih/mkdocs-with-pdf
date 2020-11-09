// Convert from '.mermaid>svg' to embedded img

const isSVGSVGElement = (element: any): element is SVGSVGElement =>
  (element instanceof SVGSVGElement);

const convertSVGto = (svgElement: SVGSVGElement) => {
  // Create canvas for converting image to data URL
  const image = document.createElement("img");
  const parent = svgElement.parentElement;
  image.style.width = svgElement.width + "px";
  image.style.height = svgElement.height + "px";

  const xml = new XMLSerializer().serializeToString(svgElement);
  const svg64 = btoa(unescape(encodeURIComponent(xml)));
  const image64 = 'data:image/svg+xml;base64,' + svg64;

  // Get data URL encoding of image
  image.setAttribute("src", image64);

  parent.replaceChild(image, svgElement);
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
    flowchart: { htmlLabels: false },
    htmlLabels: false,
    mermaid: {
      callback: (id) => {
        const svgElement = document.getElementById(id);
        if (!isSVGSVGElement(svgElement)) return;
        console.log('converting svg(' + id + ') to dataUri');
        convertSVGto(svgElement);
      }
    }
  })
}
