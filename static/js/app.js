window.addEventListener('scroll', e => {
	document.documentElement.style.setProperty('--scrollTop', `${this.scrollY}px`) // Update method
})

window.setInterval(function() {
  var elem = document.getElementById('data');
  elem.scrollTop = elem.scrollHeight;
}, 5000)

gsap.registerPlugin(ScrollTrigger, ScrollSmoother)
ScrollSmoother.create({
	wrapper: ".wrapper",
	content: ".content",
	prod_wrapper: "prod_wrapper"
})