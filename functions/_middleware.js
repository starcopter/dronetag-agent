// https://developers.cloudflare.com/pages/functions/middleware/
export async function onRequest(context) {
  const email = context.request.headers.get("cf-access-authenticated-user-email");
  const country = context.request.cf.country;
  const city = context.request.cf.city;
  const method = context.request.method;
  const url = new URL(context.request.url);

  // if (url.pathname.startsWith('/setup/') && !email?.endsWith('@starcopter.com')) {
  if (url.pathname.startsWith('/setup/')) {
    return new Response(
      "Sorry, you don't have access to this page.\n" +
      `${email}, ${city} (${country}): ${method} ${url.pathname}`,
      { status: 403 }
    );
  }
  return await context.next();
}
