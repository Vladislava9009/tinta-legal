# Tinta: privacy policy

Privacy Policy for the iOS app **Tinta: Color by Number**
(`com.tinta.app`), in English, Russian and Ukrainian.

**Status: draft, not published.** The app's paywall already links to
`https://vladislava9009.github.io/tinta-legal/privacy.html`, which will 404
until this is published with GitHub Pages. Apple rejects a subscription screen
whose links do not open, so this has to be live before the app is submitted.

Source: `texts.py` (the words) -> `build.py` generates `privacy.html`.

```bash
python3 build.py
```

English is the source of truth. The other two exist so the author can read the
policy in a language she knows. Do not translate it into the app's other
languages until the English is final: every later change would have to be made
in each of them.

## What the policy says, and how that was checked

The policy is a set of claims about what the app does. They were checked against
the code and the release build on 2026-10-17, not copied from another app's
policy.

| claim | how it was checked |
| --- | --- |
| no servers of ours, no analytics, ads or tracking | no such dependency in `app/package.json`; no `fetch`, `XMLHttpRequest` or socket call in `app/src`; no `NSUserTrackingUsageDescription` in `Info.plist` |
| nothing sent to us | every `http(s)` host in the release JS bundle and native binaries was listed. All are documentation links inside error messages, or Apple and this page. One is a client for a purchase-verification service (`kit.openiap.dev`) that ships inside the purchases library and runs only when `verifyPurchaseWithProvider` is called; the app imports no `verify*` function |
| what is stored on the device | the app writes two files only: `progress/<picture>.json` (ids of coloured regions) and `store/entitlement.json` (a yes/no and a timestamp) |
| no permissions requested | the built `Info.plist` has no `*UsageDescription` key |
| purchases happen between the person and Apple | the only store calls are `initConnection`, `fetchProducts`, `requestPurchase`, `restorePurchases`, `hasActiveSubscriptions` and `finishTransaction` through StoreKit; no `appAccountToken` or other identifier is passed |
| the language setting is read on the device | `expo-localization` is used for that and nothing else |

## Keep it in step with the app

If the app ever starts sending anything anywhere — analytics, crash reports, a
sign-in, a server that checks subscriptions, purchase verification through the
library's provider service — **this policy must change first**, and the App
Store privacy answers with it.

Things that would change the policy, and that are easy to add without noticing:

- a crash-reporting or analytics SDK, even a well-meaning one;
- moving pictures to a CDN (the CDN sees the person's IP address);
- sharing a finished picture;
- turning on `verifyPurchaseWithProvider`.

## App Store Connect answers that follow from it

- **App Privacy:** *Data Not Collected*. The app collects nothing and uses no
  third-party SDK that does.
- **Privacy Policy URL:** the published address of `privacy.html`.
- **Support URL:** still needed for submission and not built here; it is the
  same generator with a different page (see `~/Developer/wow-fasting-legal`).

## Details to confirm

- The contact email and the name under it are the ones already used by the
  Wow Fasting and Tosha's Farm pages.
- The "Children" section says the app is made for a general audience and
  collects nothing from anyone. It should agree with the age rating chosen in
  App Store Connect.
- This is a draft written to be accurate to the app, not legal advice.
