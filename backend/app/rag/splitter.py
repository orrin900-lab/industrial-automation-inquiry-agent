from app.rag.loader import KnowledgeChunk, KnowledgeDocument, KnowledgeMetadata


def split_markdown_documents(
    documents: list[KnowledgeDocument], max_chars: int = 900
) -> list[KnowledgeChunk]:
    chunks: list[KnowledgeChunk] = []
    for document in documents:
        sections = _split_by_heading(document.content)
        for section_index, (section_title, section_content) in enumerate(
            sections, start=1
        ):
            section_content = section_content.strip()
            if not section_content:
                continue
            for part_index, offset in enumerate(
                range(0, len(section_content), max_chars), start=1
            ):
                chunk_id = f"{document.source_file}:{section_index}:{part_index}"
                chunks.append(
                    KnowledgeChunk(
                        content=section_content[offset : offset + max_chars],
                        metadata=KnowledgeMetadata(
                            source_file=document.source_file,
                            section_title=section_title,
                            chunk_id=chunk_id,
                            document_type=document.document_type,
                        ),
                    )
                )
    return chunks


def _split_by_heading(content: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    current_title = "Overview"
    current_lines: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            if current_lines:
                sections.append((current_title, "\n".join(current_lines)))
            current_title = line.replace("## ", "", 1).strip() or "Untitled Section"
            current_lines = [line]
        elif line.startswith("# ") and not current_lines:
            current_title = line.replace("# ", "", 1).strip() or "Overview"
            current_lines.append(line)
        else:
            current_lines.append(line)

    if current_lines:
        sections.append((current_title, "\n".join(current_lines)))
    return sections
