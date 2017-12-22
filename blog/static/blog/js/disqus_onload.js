var disqus_onload = false;
var disqus = document.createElement('script');
var alertWall = document.getElementById("alertWall");

disqus.src = 'https://soongyk-com.disqus.com/embed.js';
disqus.setAttribute('data-timestamp', +new Date());
disqus.onload = function(){
    disqus_onload = true;
}
disqus.onerror = function(){
    disqus_onload = false;
}


document.head.appendChild(disqus);
document.body.appendChild(disqus);


setTimeout(function(){
    
    if ( !disqus_onload ){
        alertWall.style.display = "block";
    }
}, 3000);

