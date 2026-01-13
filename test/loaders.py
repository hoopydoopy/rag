from ingestion.getdata import load_google_source


# ----------------------
# Real Google Sheets test
# ----------------------
def test_real_google_sheet():
    # Provide real spreadsheet ID and worksheet name
    spreadsheet_id = ""
    worksheet_name = "streamflix"

    docs = load_google_source(
        source_type="sheets",
        spreadsheet_id=spreadsheet_id,
        worksheet_name=worksheet_name,
    )

    # Inspect returned data
    print("Sheets loader output:", docs)
    assert isinstance(docs, list)
    if docs:
        assert "content" in docs[0]
        assert "metadata" in docs[0]


# ----------------------
# Real Google Docs test
# ----------------------
def test_real_google_doc():
    document_id = ""

    docs = load_google_source(
        source_type="docs",
        document_id=document_id,
    )

    print("Docs loader output:", docs)
    assert isinstance(docs, list)
    if docs:
        assert "content" in docs[0]
        assert "metadata" in docs[0]


if __name__ == "__main__":
    test_real_google_sheet()
    test_real_google_doc()
