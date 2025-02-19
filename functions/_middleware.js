// https://developers.cloudflare.com/pages/functions/middleware/
export async function onRequest(context) {
  const email = context.request.headers.get('cf-access-authenticated-user-email');
  const country = context.request.cf.country;
  const city = context.request.cf.city;
  const method = context.request.method;
  const url = new URL(context.request.url);

  if (!email?.endsWith('@example.com')) {  // TODO: change to @starcopter.com
    if (url.pathname.startsWith('/setup/')) {
      return new Response(
        `Sorry, you don't have access to this page.\n${email}, ${city} (${country}): ${method} ${url.pathname}`,
        { status: 403 }
      );
    }

    if (url.pathname === '/search/search_index.json') {
      const response = await context.next();
      const searchIndex = await response.json();

      // Filter out any entries with setup/ in the location
      searchIndex.docs = searchIndex.docs.filter(entry => !entry.location.startsWith('setup/'));

      return new Response(JSON.stringify(searchIndex), {
        headers: {
          'content-type': 'application/json',
        },
      });
    }
  }

  return await context.next();
}
