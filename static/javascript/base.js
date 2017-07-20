/**
 * Created by mowhebat on 7/10/17.
 */

function changeContent(url)
{

    var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            var el = document.createElement('div');
            el.innerHTML = this.responseText;
            document.getElementById('container').innerHTML = el.getElementsByTagName('div')[0].innerHTML;
            console.log(document.getElementsByTagName('body')[0]);
        }
    }

    xhr.open("GET", url , true);
    xhr.send();
}