upstream web_app {
    server backend:8000;
}

events {}

http {

    server {

        listen80;
        location / {

            proxy_pass http://192.168.56.104:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP #remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_forwarded_for;

        }

    }


}