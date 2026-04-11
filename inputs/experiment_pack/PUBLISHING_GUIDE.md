# Publishing Guide: GitHub Repository and Zenodo Archive

## Step-by-Step Instructions for `gates-simulation`

This guide walks through publishing the simulation code to GitHub and archiving it via Zenodo for a permanent DOI, as referenced in the manuscript.

---

## Part 1: GitHub Repository

### Step 1: Create the Repository

1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `gates-simulation`
3. **Owner**: Select `ethicalalphaaudit` (create the organisation first if needed)
4. **Description**: "Simulation code for: Operationalizing Non-Compensatory Governance Gates (JMIR Medical Informatics, under review)"
5. **Visibility**: Public
6. **Initialize**: Do NOT add README (we have our own)
7. Click **Create repository**

### Step 2: Push the Code

From your local machine, in the `gates_simulation/` directory:

```bash
# Initialise git
git init
git branch -M main

# Add all files
git add run_simulation.py
git add run_verification.py
git add run_calibration_sensitivity.py
git add report_supplementary.py
git add params_default.json
git add requirements.txt
git add Makefile
git add LICENSE
git add README.md

# Do NOT add the outputs/ directory — these are reproducible
echo "outputs/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
git add .gitignore

# Commit
git commit -m "Initial release: primary simulation and supplementary analyses

Accompanies: Brown W. Operationalizing non-compensatory governance gates:
A theory-testing simulation study of clinical AI deployment decisions.
JMIR Medical Informatics. 2026. (Under review.)

Includes:
- Primary heterogeneous model simulation
- Verification simulations (uniform, random, partial heterogeneity)
- Calibration sensitivity analyses (portfolio composition, unsafe probability)
- Supplementary results report generator"

# Add remote and push
git remote add origin https://github.com/ethicalalphaaudit/gates-simulation.git
git push -u origin main
```

### Step 3: Create a Release Tag

```bash
git tag -a v1.0.0 -m "v1.0.0: Initial release accompanying manuscript submission"
git push origin v1.0.0
```

Alternatively, use GitHub's web interface:
1. Go to repository → **Releases** → **Create a new release**
2. Tag: `v1.0.0`
3. Title: "v1.0.0: Initial release"
4. Description: Copy the commit message above
5. Click **Publish release**

---

## Part 2: Zenodo Archive (DOI)

### Step 4: Link GitHub to Zenodo

1. Go to [zenodo.org](https://zenodo.org) and sign in (create account if needed; you can sign in with GitHub)
2. Navigate to **Settings** → **GitHub** (or go to [zenodo.org/account/settings/github](https://zenodo.org/account/settings/github))
3. Find `ethicalalphaaudit/gates-simulation` in the list
4. **Toggle ON** the repository to enable automatic archiving

### Step 5: Trigger the Archive

1. Go back to GitHub and create a new release (if you haven't already):
   - **Releases** → **Create a new release**
   - Tag: `v1.0.0`
   - Title: "v1.0.0: Manuscript submission release"
   - Publish
2. Zenodo will automatically detect the release and create an archive
3. Wait 1-5 minutes, then check [zenodo.org/deposit](https://zenodo.org/deposit)

### Step 6: Edit the Zenodo Record

Once the archive appears in your Zenodo deposits:

1. Click on the deposit to edit metadata
2. Fill in:
   - **Title**: "gates-simulation: Simulation code for non-compensatory governance gates study"
   - **Authors**: Brown, Walter (Ethical Alpha Audit; ORCID: 0000-0002-6050-8522)
   - **Description**: "Reference implementation for: Brown W. Operationalizing non-compensatory governance gates: A theory-testing simulation study of clinical AI deployment decisions. JMIR Medical Informatics. 2026. Includes primary simulation, verification simulations for analytical scope conditions, and calibration sensitivity analyses."
   - **License**: MIT License
   - **Keywords**: clinical AI, governance, simulation, non-compensatory, patient safety
   - **Related identifiers**: (Add the manuscript DOI once assigned, as "is supplement to")
   - **Communities**: Consider adding to relevant Zenodo communities (e.g., "Health Informatics")
3. Click **Publish**

### Step 7: Record the DOI

Zenodo will assign a DOI in the format: `10.5281/zenodo.XXXXXXX`

Two DOIs are created:
- **Version-specific DOI** (e.g., `10.5281/zenodo.1234567`): Points to v1.0.0 specifically
- **Concept DOI** (e.g., `10.5281/zenodo.1234566`): Always resolves to the latest version

**Use the concept DOI in the manuscript** so it always points to the latest code.

### Step 8: Update the Manuscript

In the manuscript reference [15], replace the placeholder with the actual DOI:

Before:
> Brown W. gates-simulation: Simulation code for non-compensatory governance gates study. GitHub. URL: https://github.com/ethicalalphaaudit/gates-simulation [accessed 2026-03-10].

After:
> Brown W. gates-simulation: Simulation code for non-compensatory governance gates study. Zenodo. 2026. doi:10.5281/zenodo.XXXXXXX

Also update the Data Availability statement to include the DOI.

---

## Part 3: Pre-Submission Checklist

Before submitting the manuscript, verify:

- [ ] Repository is public at `https://github.com/ethicalalphaaudit/gates-simulation`
- [ ] `python run_simulation.py` reproduces all primary results
- [ ] `make supplementary` reproduces all supplementary results
- [ ] README.md Quick Start guide is accurate
- [ ] Zenodo DOI is live and resolves correctly
- [ ] Manuscript reference [15] includes the Zenodo DOI
- [ ] Data Availability statement references both GitHub URL and Zenodo DOI
- [ ] LICENSE file is present (MIT)
- [ ] No outputs/ directory is committed (results are reproducible)
- [ ] requirements.txt lists exact versions: `pip freeze > requirements.txt`

---

## Troubleshooting

**Zenodo doesn't detect my release**: Ensure the GitHub-Zenodo integration is toggled ON for your repository. Try creating the release again.

**DOI not appearing**: Zenodo processing can take up to 10 minutes. Check [zenodo.org/deposit](https://zenodo.org/deposit).

**Reviewer cannot reproduce results**: Ensure `requirements.txt` pins exact versions. Consider adding a `Dockerfile` for containerised reproducibility.

**Need to update after revision**: Push changes, create a new release tag (e.g., `v1.1.0`), and Zenodo will automatically archive the new version under the same concept DOI.
