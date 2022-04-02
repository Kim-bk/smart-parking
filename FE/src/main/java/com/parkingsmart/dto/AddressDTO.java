package com.parkingsmart.dto;

public class AddressDTO {
	
	private Long id;
	
	private String specificAddress;
	
	private String idProvince;
	
	private String idDistrict;
	
	private String idWard;

	public AddressDTO() {
		super();
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getSpecificAddress() {
		return specificAddress;
	}

	public void setSpecificAddress(String specificAddress) {
		this.specificAddress = specificAddress;
	}

	public String getIdProvince() {
		return idProvince;
	}

	public void setIdProvince(String idProvince) {
		this.idProvince = idProvince;
	}

	public String getIdDistrict() {
		return idDistrict;
	}

	public void setIdDistrict(String idDistrict) {
		this.idDistrict = idDistrict;
	}

	public String getIdWard() {
		return idWard;
	}

	public void setIdWard(String idWard) {
		this.idWard = idWard;
	}
	
	

}
