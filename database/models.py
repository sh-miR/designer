class Backbone:
    def __init__(self, name, flanks3_s, flanks3_a, flanks5_s, flanks5_a, loop_s, loop_a, miRNA_s, mirRNA_a, miRNA_length, miRNA_min, miRNA_max, structure, homogeneity, miRBase_link):
        self.name = name
        self.flanks3_s = flanks3_s
        self.flanks3_a = flanks3_a
        self.flanks5_s = flanks5_s
        self.flanks5_a = flanks5_a
        self.loop_s = loop_s
        self.loop_a = loop_a
        self.miRNA_s = miRNA_s
        self.miRNA_a = mirRNA_a
        self.miRNA_length = miRNA_length
        self.miRNA_min = miRNA_min
        self.miRNA_max = miRNA_max
        self.structure = structure
        self.homogeneity = homogeneity
        self.miRBase_link = miRBase_link

    def serialize(self):
        return {
            'name': self.name,
            'flanks3_s': self.flanks3_s,
            'flanks3_a': self.flanks3_a,
            'flanks5_s': self.flanks5_s,
            'flanks5_a': self.flanks5_a,
            'loop_s': self.loop_s,
            'loop_a': self.loop_a,
            'miRNA_s': self.miRNA_s,
            'miRNA_a': self.miRNA_a,
            'miRNA_length': self.miRNA_length,
            'miRNA_min': self.miRNA_min,
            'miRNA_max': self.miRNA_max,
            'structure': self.structure,
            'homogeneity': self.homogeneity,
            'miRBase_link': self.miRBase_link
        }
