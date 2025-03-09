upstream web_app {
    server backend:8000;
}

events {}

http {

    server {

        listen80;
        location / {

            proxy_pass http://localhost:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP #remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_forwarded_for;

            location /static/ {
                autoindex on;
                autoindex_exact_size off;
                C:\Users\R&D\Desktop\blog\src;
            }
        }

    }


}