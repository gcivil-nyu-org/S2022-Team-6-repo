const button = document.querySelector('.copy-btn')

const addToClipboard = async (link) => {
    await navigator.clipboard.writeText(link);
}

const copyLink = async (link) => {
    const copied = await addToClipboard(link)
    button.innerText = 'Copied'
    setTimeout(() => {
        button.innerText = 'Copy link'
    }, 3000)
};
var url = window.location.href;
var domain = url.replace('http://', '').replace('https://', '').split(/[/?#]/)[0];
// console.log(domain + '/circle' + button.value);
button.addEventListener('click', () => copyLink(domain + button.value))