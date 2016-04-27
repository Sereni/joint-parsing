def extract_features(c):
    """
    Represent configuration as a feature vector.
    Assume the stack and the buffer front is always disambiguated.
    For other positions, if tokens are ambiguous, return:
        pos features: ambiguity class for all possible tokens
        form: form of surface token
    """

    # note: you may have singular tokens in the buffer
    # if you disambiguated buffer front into 3 tokens,
    # the first 3 tokens on the buffer are single

    # check each time I guess

    def ambiguity_class(tokens):
        """
        Given a list of lists of ambiguous tokens,
        concatenate all POS tags into an "ambiguity class".
        Sort tags alphabetically in the outer list.
        """
        tags = []
        for token_group in tokens:  # a group is 1 or more tokens that constitute one analysis
            group_tag = '|'.join(token.postag for token in token_group)
            tags.append(group_tag)

        return '||'.join(sorted(set(tags)))

    def form_of_buffer_front():
        return c.sentence[c.buffer[0]].form

    def pos_of_buffer_front():
        return c.sentence[c.buffer[0]].postag

    def form_of_stack_top():
        try:
            return c.sentence[c.stack[-1]].form
        except IndexError:
            return 'None'

    def pos_of_stack_top():
        try:
            return c.sentence[c.stack[-1]].postag
        except IndexError:
            return 'None'

    def pos_of_second_buffer_item():
        try:
            return c.sentence[c.buffer[1]].postag
        except IndexError:
            return 'None'
        except AttributeError:
            return ambiguity_class(c.buffer[1][1])

    def pos_of_second_stack_item():
        try:
            return c.sentence[c.stack[-2]].postag
        except IndexError:
            return 'None'

    def pos_of_leftmost_dep_of_buffer_front():
        try:
            feature = c.sentence[min({arc for arc in c.arcs if arc.h == c.buffer[0]}, key=lambda arc: arc.d).d].postag
        except ValueError:
            feature = 'None'
        return feature

    def pos_of_stack_top_and_pos_of_buffer_front():
        try:
            return pos_of_stack_top() + ' ' + pos_of_buffer_front()
        except IndexError:
            return 'None'

    def pos_of_stack_top_and_form_of_buffer_front():
        try:
            return pos_of_stack_top() + ' ' + form_of_buffer_front()
        except IndexError:
            return 'None'

    def form_of_stack_top_and_pos_of_buffer_front():
        try:
            return form_of_stack_top() + ' ' + pos_of_buffer_front()
        except IndexError:
            return 'None'

    def form_of_stack_top_and_form_of_buffer_front():
        try:
            return form_of_stack_top() + ' ' + form_of_buffer_front()
        except IndexError:
            return 'None'

    # extra features from Kuebler's book
    def lemma_stk0():
        try:
            return c.sentence[c.stack[-1]].lemma
        except IndexError:
            return 'None'

    def lemma_buf0():
        return c.sentence[c.buffer[0]].lemma

    def form_buf1():
        try:
            return c.sentence[c.buffer[1]].form
        except AttributeError:
            return c.sentence[c.buffer[1][1]].form
        except IndexError:
            return 'None'

    def pos_buf2():
        try:
            return c.sentence[c.buffer[2]].postag
        except IndexError:
            return 'None'
        except AttributeError:
            return ambiguity_class(c.sentence[c.buffer[1]])

    def pos_buf3():
        try:
            return c.sentence[c.buffer[3]].postag
        except IndexError:
            return 'None'
        except AttributeError:
            return ambiguity_class(c.sentence[c.buffer[3]])

    def deprel_rdep_stk0():
        try:
            feature = c.sentence[max(
                {arc for arc in c.arcs if arc.h == c.stack[-1]}, key=lambda arc: arc.d).d].deprel
        except ValueError:
            feature = 'None'
        except IndexError:
            feature = 'None'
        return feature

    def deprel_rdep_buf0():
        try:
            feature = c.sentence[max(
                {arc for arc in c.arcs if arc.h == c.buffer[0]}, key=lambda arc: arc.d).d].deprel
        except ValueError:
            feature = 'None'
        return feature

    def deprel_ldep_stk0():
        try:
            feature = c.sentence[min(
                {arc for arc in c.arcs if arc.h == c.stack[-1]}, key=lambda arc: arc.d).d].deprel
        except ValueError:
            feature = 'None'
        except IndexError:
            feature = 'None'
        return feature

    def deprel_ldep_buf0():
        try:
            feature = c.sentence[min(
                {arc for arc in c.arcs if arc.h == c.buffer[0]}, key=lambda arc: arc.d).d].deprel
        except ValueError:
            feature = 'None'
        return feature

    def deprel_stk0():
        try:
            return c.sentence[c.stack[-1]].deprel
        except IndexError:
            return 'None'

    def form_of_stack_top_head():
        try:
            for arc in c.arcs:
                if arc.d == c.stack[-1]:
                    return arc.h.form
        except IndexError:
            return 'None'
        return 'None'

    # ~~~~~~~~~~~~~~~~~~~~ morphological features
    # these return a list of features instead of a single one
    def morph_of_buffer_front():
        morph = c.sentence[c.buffer[0]].feats.split('|')
        return [('b0.morph{0}'.format(i), morph[i]) for i in range(len(morph))]

    def morph_of_stack_top():
        try:
            morph = c.sentence[c.stack[-1]].feats.split('|')
        except IndexError:
            return []

        return [('s0.morph{0}'.format(i), morph[i]) for i in range(len(morph))]

    def morph_string_of_buffer_front():
        morph = c.sentence[c.buffer[0]].feats
        return [('b0.morph_string', morph)]

    def morph_string_of_stack_top():
        try:
            morph = c.sentence[c.stack[-1]].feats
        except IndexError:
            return []
        return [('s0.morph_string', morph)]

    def morph_of_second_stack_item():
        try:
            morph = c.sentence[c.stack[-2]].feats.split('|')
        except IndexError:
            return []
        return [('s1.morph{0}'.format(i), morph[i]) for i in range(len(morph))]

    def morph_of_second_buffer_item():
        try:
            morph = c.sentence[c.buffer[1]].feats.split('|')
        except IndexError:
            return []
        except AttributeError:
            return []
        return [('b1.morph{0}'.format(i), morph[i]) for i in range(len(morph))]

    def morph_of_third_buffer_item():
        try:
            morph = c.sentence[c.buffer[2]].feats.split('|')
        except IndexError:
            return []
        except AttributeError:
            return []
        return [('b2.morph{0}'.format(i), morph[i]) for i in range(len(morph))]

    def get_all_morph_features():
        feats = morph_of_stack_top() + morph_of_second_stack_item() + morph_of_buffer_front() + \
                morph_of_second_buffer_item() + morph_of_third_buffer_item() \
                + morph_string_of_buffer_front() \
                + morph_string_of_stack_top()

        return dict(feats)

    morph_features = get_all_morph_features()

    feature_dict = dict(zip(
            (
                'b0.form',
                'b0.pos',
                's0.form',
                's0.pos',
                'b1.pos',
                's1.pos',
                'ld(b0).pos',
                's0.pos b0.pos',
                's0.pos b0.form',
                's0.form b0.pos',
                's0.form b0.form',
                's0.lemma',
                'b0.lemma',
                'b1.form',
                'b2.pos',
                'b3.pos',
                'rd(s0).deprel',
                'ld(s0).deprel',
                'rd(b0).deprel',
                'ld(b0).deprel',
                's0.deprel',
                's0_head.form'
            ),
            (
                form_of_buffer_front(),
                pos_of_buffer_front(),
                form_of_stack_top(),
                pos_of_stack_top(),
                pos_of_second_buffer_item(),
                pos_of_second_stack_item(),
                pos_of_leftmost_dep_of_buffer_front(),
                pos_of_stack_top_and_form_of_buffer_front(),
                form_of_stack_top_and_pos_of_buffer_front(),
                form_of_stack_top_and_form_of_buffer_front(),
                lemma_stk0(),
                lemma_buf0(),
                form_buf1(),
                pos_buf2(),
                pos_buf3(),
                deprel_rdep_stk0(),
                deprel_ldep_stk0(),
                deprel_rdep_buf0(),
                deprel_ldep_buf0(),
                deprel_stk0(),
                form_of_stack_top_head()
            )
        ))
    feature_dict.update(morph_features)
    return feature_dict