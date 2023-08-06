class TagsSupport:
    @staticmethod
    def getTagsInFacet(tags, facet):
        res = set()
        for tag in tags:
            if tag.startswith(facet + '.'):
                res.add(tag)

    @staticmethod
    def getFirstTag(tags, facet):
        for tag in tags:
            if tag.startswith(facet + '.'):
                dot_index = tag.index('.')
                return tag[dot_index:]
        return None
