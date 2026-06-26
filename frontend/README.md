# Industrial Inquiry Agent Frontend

Next.js App Router MVP for customer service and export sales users.

## Features

- Dashboard with backend health and recent inquiry stats
- Website and email inquiry analysis form
- Sample inquiry loading from the FastAPI backend
- Inquiry list with status and channel filters
- Inquiry detail view with AgentResult, candidate products, missing information, retrieved knowledge, and execution trace
- Editable English reply draft
- Human review submission

The frontend does not send emails, quote prices, promise stock, or promise lead time.

## Docker

The frontend is included in the root Docker Compose stack:

```bash
cd ..
docker compose up --build
```

If `docker compose` is unavailable locally:

```bash
cd ..
docker-compose up --build
```

Docker maps the frontend container port `3000` to the host port `3001`.

Open:

```text
http://127.0.0.1:3001
```

The browser-facing API base URL is baked into the Docker build as:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## Environment

Create `.env.local` from `.env.example` when needed:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## Run

```bash
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

If port 3000 is already in use, run the frontend on 3001:

```bash
npm run dev -- -p 3001
```

Open:

```text
http://localhost:3001
```

If another local service already owns `localhost:3001`, bind this project to IPv4 explicitly:

```bash
npm run dev -- -H 127.0.0.1 -p 3001
```

Open:

```text
http://127.0.0.1:3001
```

## Build

```bash
npm run build
```

## Docker Stop

From the project root:

```bash
docker compose down
```

Clear the PostgreSQL volume:

```bash
docker compose down -v
```

## Troubleshooting

- If `'next' is not recognized`, run `npm install` first.
- If port 3000 is already in use, run `npm run dev -- -p 3001`.
- If `localhost:3001` is already occupied by another local project, run `npm run dev -- -H 127.0.0.1 -p 3001`.
- If the frontend cannot call the API, confirm the FastAPI backend is running at `http://127.0.0.1:8000` and CORS allows the current frontend port.
