pragma solidity ^0.5.0;

// import "/home/ubuntu/artwork_token/contracts/openzeppelin-contracts-release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "/Users/michaelcruz/git/artwork_token/contracts/openzeppelin-contracts-release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract Certificate is ERC721Full {
    constructor() public ERC721Full("Certificate", "CERT") {}

    function awardCertificate(address student, string memory tokenURI)
        public
        returns (uint256)
    {
        uint256 newCertificateId = totalSupply();
        _mint(student, newCertificateId);
        _setTokenURI(newCertificateId, tokenURI);

        return newCertificateId;
    }
}
