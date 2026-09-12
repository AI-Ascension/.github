# Reusable CI pilot

Run the local producer/consumer contract with:

```bash
bash reusable-ci/pilot/producer.sh /tmp/reusable-ci-receipt.json
bash reusable-ci/pilot/consumer.sh /tmp/reusable-ci-receipt.json
```

The caller uses a same-repository relative workflow only for this pilot. No published
workflow revision exists, so no consumer is given an invented remote SHA. After an
owner authorizes publication and the hosted pilot succeeds, consumers should adopt
`AI-Ascension/.github/.github/workflows/reusable-ci-pilot.yml@<published-immutable-SHA>`
in one canary, then progressively; rollback is restoration of the prior SHA.
