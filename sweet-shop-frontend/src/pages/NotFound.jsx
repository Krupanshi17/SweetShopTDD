export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-background">
      <h1 className="text-red-500 text-4xl font-bold">404 - Page Not Found</h1>
      <a href="/" className="text-blue-500 mt-4 underline">
        Go Home
      </a>
    </div>
  );
}
