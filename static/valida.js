document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('cadastroForm');

  form.addEventListener('submit', function (e) {
    e.preventDefault(); 

    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const senhaRegex = /^(?=.*[A-Z])(?=.*\d).{8,}$/;

    if (nome.length < 3) {
      alert("O nome deve ter pelo menos 3 caracteres.");
      return;
    }

    if (!emailRegex.test(email)) {
      alert("E-mail inválido.");
      return;
    }

    if (!senhaRegex.test(senha)) {
      alert("A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula e um número.");
      return;
    }

    form.classList.add('fade-out');

    setTimeout(() => {
      form.submit();
    }, 500); 
  });
});
