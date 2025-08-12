const personagem = document.querySelector('.personagem')


const jump = () => {
    personagem.classList.add('jump');
    setTimeout(() =>{
        personagem.classList.remove('jump');
    }, 500);
}
document.addEventListener('keydown', jump)