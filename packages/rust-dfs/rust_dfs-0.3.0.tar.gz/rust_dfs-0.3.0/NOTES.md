# Notes

## How to do a release

It should be ok to do this in main branch.

Update `RELEASE.md` with changes since last release. These may be of 4 categories:

- *Python*: only affects python code
- *Rust*: only affects rust code
- *Shared*: affects both python and rust code
- *Other*: something else

```markdown
## [0.3.0] - 2022-12-17
### Shared
- Serialize and Deserialize Features and Primitives (#8)

## [0.2.0] - 2022-07-30
### Other
- adding action to deploy docs
### Rust
- removed `input_set` in favor of `column_schema`(#5)
- created a hashmap that keys by both logical_type and semantic_tag and then finds set interception between them for matching features to a primitive (#5)
- primitive types that can't be found are tagged as "Any". So a Primitive that has an input of ["", "Numeric"], can match to a feature that has any logical_type and a semantic tag of Numeric. (#5)
- removed a lot of references in place of `.clone()`. This will need to be revisited. (#5)
- created directory for feature related code (#5)
### Python
- added `time_index` argument to `generate_fake_dataframe` to create a time index (#5)
- fixed tests to test all logical types (#5)
````