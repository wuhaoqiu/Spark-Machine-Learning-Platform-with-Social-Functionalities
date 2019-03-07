(function(){
    //check whether the myBookmarklet is created, if not, create one, otherwise, invoke another js file called bookmarklet.js using a random number
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }else {
        // document.body.appendChild(document.createElement('script')).src= 'http://127.0.0.1:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
        document.body.appendChild(document.createElement('script')).src= 'http://38a1dc54.ngrok.io/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();