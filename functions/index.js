// Webhook de Stripe → Firestore.
// Activa o desactiva Premium en users/{uid} cuando Stripe confirma un pago o cancela una suscripción.
//
// Despliegue (requiere el plan Blaze de Firebase):
//   firebase functions:secrets:set STRIPE_SECRET_KEY        (sk_test_... o sk_live_...)
//   firebase functions:secrets:set STRIPE_WEBHOOK_SECRET    (whsec_...)
//   firebase deploy --only functions
// Después, en Stripe → Developers → Webhooks, agrega la URL de la función con los eventos:
//   checkout.session.completed, customer.subscription.deleted
const { onRequest } = require('firebase-functions/v2/https');
const { defineSecret } = require('firebase-functions/params');
const admin = require('firebase-admin');
const Stripe = require('stripe');

admin.initializeApp();
const db = admin.firestore();
const STRIPE_SECRET_KEY = defineSecret('STRIPE_SECRET_KEY');
const STRIPE_WEBHOOK_SECRET = defineSecret('STRIPE_WEBHOOK_SECRET');

// Montos en centavos de MXN: deben coincidir con los precios de los enlaces de pago.
const PLANES = { 19900: { plan: 'mensual', dias: 30 }, 159900: { plan: 'anual', dias: 365 } };

exports.stripeWebhook = onRequest({ secrets: [STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET], region: 'us-central1' }, async (req, res) => {
  const stripe = Stripe(STRIPE_SECRET_KEY.value());
  let event;
  try {
    // Verifica que el aviso venga de Stripe (firma del webhook).
    event = stripe.webhooks.constructEvent(req.rawBody, req.headers['stripe-signature'], STRIPE_WEBHOOK_SECRET.value());
  } catch (err) {
    console.error('Firma inválida:', err.message);
    return res.status(400).send('Firma inválida');
  }

  try {
    if (event.type === 'checkout.session.completed') {
      const s = event.data.object;
      const uid = s.client_reference_id; // planes.html lo agrega al enlace de pago
      if (!uid || s.payment_status !== 'paid') return res.json({ ignorado: true });
      const info = PLANES[s.amount_total] || { plan: 'mensual', dias: 30 };
      const exp = new Date(); exp.setDate(exp.getDate() + info.dias);
      await db.doc(`users/${uid}`).set({
        isPremium: true,
        tipoPlan: info.plan,
        fechaExpiracion: admin.firestore.Timestamp.fromDate(exp),
        stripeCustomerId: s.customer || null,
        ultimoPago: admin.firestore.FieldValue.serverTimestamp(),
      }, { merge: true });
    }

    if (event.type === 'customer.subscription.deleted') {
      const customer = event.data.object.customer;
      const qs = await db.collection('users').where('stripeCustomerId', '==', customer).get();
      await Promise.all(qs.docs.map((d) => d.ref.set({ isPremium: false }, { merge: true })));
    }
    res.json({ recibido: true });
  } catch (err) {
    console.error('Error al actualizar Firestore:', err);
    res.status(500).send('Error interno');
  }
});
