var imgs = document.getElementsByTagName('img');

for(var i=0; i<imgs.length; i++) {
    if (imgs[i].hasAttribute('class')) {
        if (imgs[i].getAttribute('class') == "preview") {
            imgs[i].setAttribute('alt', "Document selected");
        } //if
    } //if
} //for
